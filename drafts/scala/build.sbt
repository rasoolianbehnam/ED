name := "BasicProjectWithScalaTest"

version := "1.0"

scalaVersion := "2.10.0"

// https://mvnrepository.com/artifact/org.nd4j/nd4j-native-platform
libraryDependencies += "org.nd4j" % "nd4j-native-platform" % "1.0.0-alpha"

// https://mvnrepository.com/artifact/org.nd4j/nd4s
libraryDependencies += "org.nd4j" %% "nd4s" % "1.0.0-alpha"

// https://mvnrepository.com/artifact/org.datavec/datavec-spark
libraryDependencies += "org.datavec" %% "datavec-spark" % "1.0.0-alpha_spark_1"

// https://mvnrepository.com/artifact/org.bytedeco.javacpp-presets/opencv
libraryDependencies += "org.bytedeco.javacpp-presets" % "opencv" % "3.4.3-1.4.3"

