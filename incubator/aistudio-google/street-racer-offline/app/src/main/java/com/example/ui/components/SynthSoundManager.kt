package com.example.ui.components

import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioManager
import android.media.AudioTrack
import android.os.Build
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlin.math.sin

class SynthSoundManager {
    private val scope = CoroutineScope(Dispatchers.Default)
    private var engineTrack: AudioTrack? = null
    private var engineJob: Job? = null
    private var isMuted = false
    private var engineBaseFreq = 90f
    private var targetFreq = 90f

    init {
        startEngineSound()
    }

    fun setMute(muted: Boolean) {
        this.isMuted = muted
        if (muted) {
            try { engineTrack?.pause() } catch (_: Exception) {}
        } else {
            try { engineTrack?.play() } catch (_: Exception) {}
        }
    }

    fun updateEnginePitch(speedRatio: Float) {
        // speedRatio is between 0.0f and 1.0f
        targetFreq = 80f + (speedRatio * 180f)
    }

    private fun startEngineSound() {
        engineJob = scope.launch {
            val sampleRate = 22050
            val bufferSize = AudioTrack.getMinBufferSize(
                sampleRate,
                AudioFormat.CHANNEL_OUT_MONO,
                AudioFormat.ENCODING_PCM_8BIT
            ).coerceAtLeast(512)

            val track = try {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    AudioTrack.Builder()
                        .setAudioAttributes(
                            AudioAttributes.Builder()
                                .setUsage(AudioAttributes.USAGE_MEDIA)
                                .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                                .build()
                        )
                        .setAudioFormat(
                            AudioFormat.Builder()
                                .setEncoding(AudioFormat.ENCODING_PCM_8BIT)
                                .setSampleRate(sampleRate)
                                .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                                .build()
                        )
                        .setBufferSizeInBytes(bufferSize)
                        .setTransferMode(AudioTrack.MODE_STREAM)
                        .build()
                } else {
                    @Suppress("DEPRECATION")
                    AudioTrack(
                        AudioManager.STREAM_MUSIC,
                        sampleRate,
                        AudioFormat.CHANNEL_OUT_MONO,
                        AudioFormat.ENCODING_PCM_8BIT,
                        bufferSize,
                        AudioTrack.MODE_STREAM
                    )
                }
            } catch (e: Exception) {
                e.printStackTrace()
                null
            }

            if (track == null) return@launch
            engineTrack = track
            try { track.play() } catch (_: Exception) { return@launch }

            val buffer = ByteArray(256)
            var angle = 0.0

            while (true) {
                if (isMuted) {
                    delay(100)
                    continue
                }
                
                // Linear frequency smoothing
                engineBaseFreq = (engineBaseFreq * 0.85f) + (targetFreq * 0.15f)
                val freq = engineBaseFreq
                
                for (i in buffer.indices) {
                    val value = sin(angle)
                    // Synthesize rich sounding square-adjacent sine wave
                    buffer[i] = (value * 25 + 127).toInt().toByte()
                    angle += 2.0 * Math.PI * freq / sampleRate
                    if (angle > 2.0 * Math.PI) {
                        angle -= 2.0 * Math.PI
                    }
                }
                
                try {
                    track.write(buffer, 0, buffer.size)
                } catch (e: Exception) {
                    break
                }
                delay(6)
            }
        }
    }

    fun playCoinSound() {
        if (isMuted) return
        scope.launch {
            val sampleRate = 22050
            val duration = 0.15f
            val numSamples = (sampleRate * duration).toInt()
            val buffer = ByteArray(numSamples)
            
            for (i in 0 until numSamples) {
                val progress = i.toFloat() / numSamples
                val freq = if (progress < 0.4f) 720f else 1150f
                val sampleValue = sin(2.0 * Math.PI * freq * i / sampleRate)
                buffer[i] = (sampleValue * 45 + 127).toInt().toByte()
            }
            playPcm(buffer, sampleRate)
        }
    }

    fun playCrashSound() {
        if (isMuted) return
        scope.launch {
            val sampleRate = 22050
            val duration = 0.25f
            val numSamples = (sampleRate * duration).toInt()
            val buffer = ByteArray(numSamples)
            
            for (i in 0 until numSamples) {
                val progress = i.toFloat() / numSamples
                val decay = 1.0f - progress
                val noise = (Math.random() * 2.0 - 1.0)
                buffer[i] = (noise * 55 * decay + 127).toInt().toByte()
            }
            playPcm(buffer, sampleRate)
        }
    }

    fun playNitroSound() {
        if (isMuted) return
        scope.launch {
            val sampleRate = 22050
            val duration = 0.35f
            val numSamples = (sampleRate * duration).toInt()
            val buffer = ByteArray(numSamples)
            
            for (i in 0 until numSamples) {
                val progress = i.toFloat() / numSamples
                val decay = 1.0f - progress
                val freqSweep = 1800f - (progress * 1300f)
                val wave = sin(2.0 * Math.PI * freqSweep * i / sampleRate)
                val noise = (Math.random() * 2.0 - 1.0)
                val finalVal = (wave * 0.4f + noise * 0.6f) * 45 * decay
                buffer[i] = (finalVal + 127).toInt().toByte()
            }
            playPcm(buffer, sampleRate)
        }
    }

    fun playBeepLow() {
        if (isMuted) return
        scope.launch {
            val sampleRate = 22050
            val duration = 0.15f
            val numSamples = (sampleRate * duration).toInt()
            val buffer = ByteArray(numSamples)
            for (i in 0 until numSamples) {
                val sampleValue = sin(2.0 * Math.PI * 415f * i / sampleRate)
                buffer[i] = (sampleValue * 35 + 127).toInt().toByte()
            }
            playPcm(buffer, sampleRate)
        }
    }

    fun playBeepHigh() {
        if (isMuted) return
        scope.launch {
            val sampleRate = 22050
            val duration = 0.3f
            val numSamples = (sampleRate * duration).toInt()
            val buffer = ByteArray(numSamples)
            for (i in 0 until numSamples) {
                val sampleValue = sin(2.0 * Math.PI * 830f * i / sampleRate)
                buffer[i] = (sampleValue * 35 + 127).toInt().toByte()
            }
            playPcm(buffer, sampleRate)
        }
    }

    fun playVictorySound() {
        if (isMuted) return
        scope.launch {
            val sampleRate = 22050
            val notes = listOf(523f, 659f, 784f, 1046f) // C5, E5, G5, C6
            val noteDuration = 0.12f
            val numSamples = (sampleRate * noteDuration).toInt()
            
            val fullBuffer = ByteArray(numSamples * notes.size)
            for ((nIdx, freq) in notes.withIndex()) {
                val offset = nIdx * numSamples
                for (i in 0 until numSamples) {
                    val sampleValue = sin(2.0 * Math.PI * freq * i / sampleRate)
                    fullBuffer[offset + i] = (sampleValue * 35 + 127).toInt().toByte()
                }
            }
            playPcm(fullBuffer, sampleRate)
        }
    }

    private fun playPcm(buffer: ByteArray, sampleRate: Int) {
        try {
            val track = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                AudioTrack.Builder()
                    .setAudioAttributes(
                        AudioAttributes.Builder()
                            .setUsage(AudioAttributes.USAGE_MEDIA)
                            .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                            .build()
                    )
                    .setAudioFormat(
                        AudioFormat.Builder()
                            .setEncoding(AudioFormat.ENCODING_PCM_8BIT)
                            .setSampleRate(sampleRate)
                            .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                            .build()
                    )
                    .setBufferSizeInBytes(buffer.size)
                    .setTransferMode(AudioTrack.MODE_STATIC)
                    .build()
            } else {
                @Suppress("DEPRECATION")
                AudioTrack(
                    AudioManager.STREAM_MUSIC,
                    sampleRate,
                    AudioFormat.CHANNEL_OUT_MONO,
                    AudioFormat.ENCODING_PCM_8BIT,
                    buffer.size,
                    AudioTrack.MODE_STATIC
                )
            }
            track.write(buffer, 0, buffer.size)
            track.play()
            
            scope.launch {
                delay((buffer.size.toFloat() / sampleRate * 1000 + 150).toLong())
                try {
                    track.stop()
                    track.release()
                } catch (_: Exception) {}
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun release() {
        engineJob?.cancel()
        try {
            engineTrack?.stop()
            engineTrack?.release()
        } catch (_: Exception) {}
    }
}
