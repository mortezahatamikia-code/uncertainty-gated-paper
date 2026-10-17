# ProGuard rules for BioDINO-Edge

# Keep ONNX Runtime JNI bindings and native interfaces
-keep class ai.onnxruntime.** { *; }
-dontwarn ai.onnxruntime.**

# Keep CameraX internal delegates
-keep class androidx.camera.** { *; }

# Keep data models
-keep class com.biodino.edge.domain.model.** { *; }
