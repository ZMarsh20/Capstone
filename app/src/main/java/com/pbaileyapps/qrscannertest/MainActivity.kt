package com.pbaileyapps.qrscannertest

import android.content.Intent
import android.media.MediaPlayer
import android.os.Bundle
import android.util.Log
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.google.zxing.integration.android.IntentIntegrator
import java.io.*
import java.net.URL
import java.net.URLConnection
import kotlin.concurrent.thread

class MainActivity : AppCompatActivity() {

    lateinit var eventCode: EditText
    lateinit var cameraCode: Switch
    var clickBool = false
    var camera = 0



    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        eventCode = findViewById(R.id.eventCode)
        cameraCode = findViewById(R.id.switchCamera)
        val qrButton:Button = findViewById(R.id.qr_button)




        qrButton.setOnClickListener({

            if (cameraCode.isChecked()){
                camera = 0
            }else{
                camera = 1
            }
            clickBool = true
            val intentIntegrator = IntentIntegrator(this)
            intentIntegrator.setDesiredBarcodeFormats(listOf(IntentIntegrator.QR_CODE))
            intentIntegrator.setCameraId(camera)
            intentIntegrator.initiateScan()
        })
    }

    override fun onResume() {
        super.onResume()
        if (clickBool == true){
            //Log.v("HERE", "HERE")
            val intentIntegrator = IntentIntegrator(this)
            intentIntegrator.setDesiredBarcodeFormats(listOf(IntentIntegrator.QR_CODE))
            intentIntegrator.setCameraId(camera)
            intentIntegrator.initiateScan()
        }

    }

    fun toasty() {
        Toast.makeText(applicationContext,"Something went wrong.\nPlease try again.",Toast.LENGTH_SHORT).show()
        clickBool = false

    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        val result = IntentIntegrator.parseActivityResult(resultCode, data)
        if (result != null) {

            Log.v("Debug", "postdata = ${result.contents}\n")


            thread(start = true) {

                try {

                    val url = URL("https://victorf8.pythonanywhere.com/submit-attendance")
                    var postData = "s=${result.contents}"

                    //Log.v("Debug", "postdata = ${postData} \n")

                    postData = postData.replace("#", eventCode.text.toString())

                    val conn: URLConnection = url.openConnection()
                    //conn.connect()
                    conn.setDoOutput(true)
                    conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded")
                    conn.setRequestProperty("Content-Length", Integer.toString(postData.length))

                    Log.v("Debug", "postdata = ${postData} \n")

                    DataOutputStream(conn.getOutputStream()).use { dos -> dos.writeBytes(postData) }
                    //var dos = DataOutputStream(conn.getOutputStream())
                    //dos.writeBytes(postData)
                    //dos.flush()
                    Log.v("Debug", "${postData} sent as POST request to ${url} \n")

                    BufferedReader(
                        InputStreamReader(
                            conn.getInputStream()
                        )
                    ).use { bf ->
                        var line: String?
                        while (bf.readLine().also { line = it } != null) {
                            Log.v("Debug", "Server returned: ${line} \n")

                            if (line == "failure"){
                                val mp: MediaPlayer = MediaPlayer.create(applicationContext, R.raw.beep)
                                mp.start()
                                //do bad stuff handler looper
                            }

                        }
                    }

                }catch(e: Exception){

                    Log.v("Debug", " ${e} \n")

                    val mp: MediaPlayer = MediaPlayer.create(applicationContext, R.raw.beep)
                    mp.start()

                    //toasty()
                }

            }





        }
    }

//    private fun shit() {
//        val result = IntentIntegrator.parseActivityResult(resultCode, data)
//        if (result != null) {
//
//
//            thread(start = true) {
//
//                val url = URL("https://victorf8.pythonanywhere.com/submit-attendance")
//                val postData = "${result.contents}"
//
//                val conn: URLConnection = url.openConnection()
//                conn.setDoOutput(true)
//                conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded")
//                conn.setRequestProperty("Content-Length", Integer.toString(postData.length))
//
//                DataOutputStream(conn.getOutputStream()).use { dos -> dos.writeBytes(postData) }
//
////                    BufferedReader(
////                        InputStreamReader(
////                            conn.getInputStream()
////                        )
////                    ).use { bf ->
////                        var line: String?
////                        while (bf.readLine().also { line = it } != null) {
////                            println(line)
////                        }
////                    }
//
//            }
//        }
//    }

}