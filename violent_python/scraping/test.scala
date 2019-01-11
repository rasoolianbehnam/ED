import java.io.File
val f = new File("./")
println(f.listFiles.filter(_.toString.endsWith("jpg")).mkString(" "))
