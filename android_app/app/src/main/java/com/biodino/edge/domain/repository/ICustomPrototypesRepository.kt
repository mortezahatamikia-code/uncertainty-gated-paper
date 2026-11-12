package com.biodino.edge.domain.repository

import com.biodino.edge.domain.model.CustomEnrolledDisease
import kotlinx.coroutines.flow.StateFlow

/**
 * Domain contract for persisting and observing custom enrolled prototype classes.
 */
interface ICustomPrototypesRepository {
    val customPrototypes: StateFlow<List<CustomEnrolledDisease>>

    fun enrollNewDisease(
        commonName: String,
        hostPlant: String,
        latinName: String,
        isHealthy: Boolean,
        symptom: String,
        advice: String,
        calibratedPrototype: FloatArray
    ): CustomEnrolledDisease

    fun deleteCustomDisease(id: String)
    fun clearAll()
}
