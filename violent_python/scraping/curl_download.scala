import scala.collection.mutable._  
import scala.sys.process._
import java.io.File

object curl_download extends App{
/* User provided */
var curl_original = """curl 'https://s29.openstream.io/hls/qvsbdvflndblgwsztqekayofkc3dkdpuhxce4tsdjtjuj7vrh6rwq42agxlq/seg-%s-v1-a1.jpg' -H 'Origin: https://embed.streamx.me' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.116' -H 'Accept: */*' -H 'Referer: https://embed.streamx.me/?k=3da769b6aeb4a0d043107299e356304a&li=0&tham=1548810901&lt=os&st=5b59af664b9f90b4d00f73cc3916bb6639f1887f6906d8baf42f1af02624db0767400d97a877adfc3bc0d69588e08074e5198ee6e55a35e570918bf45efb4a4243401226356cf12d109ca4d729395ebf263a99bc8bdd5975df50115bfb316fe79929358b23838c2a0b2f132e443d42e4973dc0d6f17889e485427583e7ad2139&qlt=720p&spq=p&prv=&key=38e521c260b83b0b7b9731cae1be3257&h=1548810901&w=100%&h=675' -H 'Connection: keep-alive' --compressed -O 2> /dev/null""" 
curl_original = "echo " + curl_original
val numberFormat = "%d"
val maxNumber = 3

val minNumber = 1
val numThreads = 2
/* End of User input */

val q = Queue[Int]()
for (i <- minNumber to maxNumber) q.enqueue(i)
val curl = curl_original.format(numberFormat)

def createThread(block: => Unit) = 
    new Thread {
        override def run() { block }
    }
def block() {
    var a: Int = 0
    val p = Process("/bin/bash", new File("./"), ("LANG", "en_US"))
    while (q.size != 0) {
        q.synchronized {
            a = q.dequeue()
        }
        val b = (curl.format(a) #| p).!
        System.out.synchronized {
        if (b != 0) println(a + " Unsuccessful!")
                else println(a + " Successful")
        }
    }
}

val threads = for (i <- 1 to numThreads) yield createThread(block)
for (thread <- threads) thread.start()
}
