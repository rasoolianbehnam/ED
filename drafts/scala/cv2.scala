package org.complements.behnam

import org.nd4s.Implicits._
import org.nd4j.linalg.factory.Nd4j
import org.nd4j.linalg.api.ndarray.INDArray
import org.nd4j.linalg.api.ndarray.INDArray
import org.datavec.image.loader.NativeImageLoader
import java.awt.image.BufferedImage
import java.awt.Color
import org.nd4j.linalg.indexing.NDArrayIndex
import org.nd4j.linalg.indexing.INDArrayIndex
import org.nd4j.linalg.indexing.SpecifiedIndex

import org.bytedeco.javacpp.opencv_highgui
import org.bytedeco.javacpp.opencv_core._
import org.bytedeco.javacpp.opencv_core
import org.bytedeco.javacpp.opencv_imgproc


import scala.collection.mutable.ArrayBuffer
object cv2 {
    def resize(img: Mat, s: (Int, Int)) = {
        val size = img.size
        val newSize = new Size(s._1, s._2)
        val img3 = new Mat(newSize)
        opencv_imgproc.resize(img, img3, newSize)
        img3
    }
    def asImage(image: INDArray): BufferedImage = {
        val shape = for (x <- image.shape()) yield x.asInstanceOf[Int]
        val (w, h, d) = shape match {
            case Array(1, d, w, h) => (w, h, d)
            case Array(d, w, h) => (w, h, d)
            case Array(w, h) => (w, h, 1)
        }
        println(s"Shape is h=$h, w=$w, d=$d")
        val img = image.dup().reshape(d, w, h)
        val imageBuffer = new BufferedImage(h, w, BufferedImage.TYPE_INT_RGB)
        if (d == 1) {
            img.divi(img.max())
            img.muli(255)
        }
        for (i <- 0 until w) {
            for (j <- 0 until h) {
                if (d == 1) {
                    val v = img.getInt(0, i, j)
                    imageBuffer.setRGB(j, i, new Color(v, v, v).getRGB)
                }
                else {
                    val Array(r, g, b) = img.get(NDArrayIndex.all(), 
                                     NDArrayIndex.point(i), 
                                     NDArrayIndex.point(j)).toFloatVector
                    imageBuffer.setRGB(j, i, new Color(r/255, g/255, b/255).getRGB)
                }
            }
        }
        imageBuffer
    }
    def asImage(image: Mat): BufferedImage = asImage(asMatrix(image))
    
    def asMat(img: INDArray) = {
        val (d: Int, w: Int, h: Int) = 
            img.shape match {
                case Array(1, d, w, h) => (d, w, h)
                case Array(d, w, h) =>  (d, w, h)
                case Array(w, h) => (1, w, h)
            }
        println(s"Shape is h=$h, w=$w, d=$d")
        val loader = new NativeImageLoader(h, w)
        loader.asMat(img.reshape(1, d, w, h))
    }
    def asMatrix(img: Mat) = {
        val (w, h) = (img.size.width, img.size.height)
        val loader = new NativeImageLoader(h, w)
        loader.asMatrix(img)
    }
    def erode(img: Mat, kernel: Mat) = {
        val output = img.clone()
        opencv_imgproc.erode(img, output, kernel)
        output
    }
    def dilate(img: Mat, kernel: Mat) = {
        val output = img.clone()
        opencv_imgproc.dilate(img, output, kernel)
        output
    }   
    def filter2D(img: Mat, kernel: Mat) = {
        val output = img.clone()
        opencv_imgproc.filter2D(img, output, -1, kernel)
        output
    }      
    def GaussianBlur(img: Mat, ksize: (Int, Int), sigmaX: Double) = {
        val output = img.clone 
        opencv_imgproc.GaussianBlur(img, output, new Size(ksize._1, ksize._2), sigmaX)
        output
    }
    def nonZero(img: INDArray) = {
        val matrix = asMat(img)
        matrix.convertTo(matrix, CV_8UC1)
        val vertices = new Mat()
        findNonZero(matrix, vertices)
        cv2.asMatrix(vertices)(0,->,->,0)
    }
}
