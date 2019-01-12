import scala.collection.mutable._  
import scala.sys.process._
import java.io.File

/* User provided */
var curl_original = """curl 'https://s20.7fuc.xyz/hls/qvsbcngfn7blgwsztrtka66tjmpr76uxm242ukcoqcyzewtljstdxp6tjuga/seg-%s-v1-a1.jpg' -H 'origin: https://putlocker9.nl' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.99' -H 'accept: */*' -H 'referer: https://putlocker9.nl/film/the-predator-2018-1080p.64463/watching.html' -H 'authority: s20.7fuc.xyz' --compressed -O 2> /dev/null""" 
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
