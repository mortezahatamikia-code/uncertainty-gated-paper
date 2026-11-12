package com.biodino.edge.data.repository

import android.content.Context
import android.util.Base64
import com.biodino.edge.domain.model.CustomEnrolledDisease
import com.biodino.edge.domain.repository.ICustomPrototypesRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.util.UUID

class CustomPrototypesRepository(context: Context) : ICustomPrototypesRepository {

    private val prefs = context.getSharedPreferences("biodino_custom_prototypes", Context.MODE_PRIVATE)
    private val _customPrototypes = MutableStateFlow<List<CustomEnrolledDisease>>(emptyList())
    override val customPrototypes: StateFlow<List<CustomEnrolledDisease>> = _customPrototypes.asStateFlow()

    init {
        loadFromPrefs()
    }

    private fun loadFromPrefs() {
        val raw = prefs.getString("enrolled_classes", null) ?: return
        try {
            val items = raw.split("###").filter { it.isNotBlank() }.mapNotNull { block ->
                val parts = block.split("%%%")
                if (parts.size >= 8) {
                    val id = parts[0]
                    val commonName = parts[1]
                    val hostPlant = parts[2]
                    val latin = parts[3]
                    val isHealthy = parts[4].toBoolean()
                    val symptom = parts[5]
                    val advice = parts[6]
                    val base64Embedding = parts[7]

                    val bytes = Base64.decode(base64Embedding, Base64.NO_WRAP)
                    val floatBuf = ByteBuffer.wrap(bytes).order(ByteOrder.LITTLE_ENDIAN).asFloatBuffer()
                    val embedding = FloatArray(floatBuf.remaining())
                    floatBuf.get(embedding)

                    CustomEnrolledDisease(
                        id = id,
                        commonName = commonName,
                        hostPlant = hostPlant,
                        latinTaxonomy = latin,
                        isHealthy = isHealthy,
                        primarySymptom = symptom,
                        actionableAdvice = advice,
                        prototypeEmbedding = embedding
                    )
                } else null
            }
            _customPrototypes.value = items
        } catch (_: Exception) {}
    }

    private fun saveToPrefs(items: List<CustomEnrolledDisease>) {
        val serialized = items.joinToString("###") { item ->
            val byteBuf = ByteBuffer.allocate(item.prototypeEmbedding.size * 4).order(ByteOrder.LITTLE_ENDIAN)
            byteBuf.asFloatBuffer().put(item.prototypeEmbedding)
            val base64 = Base64.encodeToString(byteBuf.array(), Base64.NO_WRAP)

            listOf(
                item.id,
                item.commonName,
                item.hostPlant,
                item.latinTaxonomy,
                item.isHealthy.toString(),
                item.primarySymptom,
                item.actionableAdvice,
                base64
            ).joinToString("%%%")
        }
        prefs.edit().putString("enrolled_classes", serialized).apply()
    }

    override fun enrollNewDisease(
        commonName: String,
        hostPlant: String,
        latinName: String,
        isHealthy: Boolean,
        symptom: String,
        advice: String,
        calibratedPrototype: FloatArray
    ): CustomEnrolledDisease {
        val newItem = CustomEnrolledDisease(
            id = UUID.randomUUID().toString(),
            commonName = commonName,
            hostPlant = hostPlant,
            latinTaxonomy = latinName,
            isHealthy = isHealthy,
            primarySymptom = symptom,
            actionableAdvice = advice,
            prototypeEmbedding = calibratedPrototype
        )

        val updated = _customPrototypes.value + newItem
        _customPrototypes.value = updated
        saveToPrefs(updated)
        return newItem
    }

    override fun deleteCustomDisease(id: String) {
        val updated = _customPrototypes.value.filter { it.id != id }
        _customPrototypes.value = updated
        saveToPrefs(updated)
    }

    override fun clearAll() {
        _customPrototypes.value = emptyList()
        prefs.edit().remove("enrolled_classes").apply()
    }
}
