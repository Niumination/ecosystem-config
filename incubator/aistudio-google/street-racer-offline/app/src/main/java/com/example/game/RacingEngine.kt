package com.example.game

import kotlin.math.*

data class CarSpec(
    val id: String,
    val name: String,
    val topSpeedKmh: Float,
    val acceleration: Float,
    val handling: Float,
    val nitroPower: Float,
    val colorHex: String,
    val price: Int
) {
    fun getTopSpeedUnits(): Float {
        return topSpeedKmh * 0.08f
    }
}

data class TrackSpec(
    val id: String,
    val name: String,
    val length: Float,
    val laps: Int = 3,
    val skyColor: String,
    val grassColor: String,
    val roadColor: String,
    val description: String,
    val obstacleDensity: Float // 0f to 1.0f
)

data class TrackObject(
    val type: Type,
    val distance: Float,
    val lateralX: Float, // -75.0f to 75.0f (0.0f is center)
    var isActive: Boolean = true
) {
    enum class Type { COIN, NITRO, BOOSTER, OBSTACLE }
}

class RacerState(
    val name: String,
    val isPlayer: Boolean,
    val carColor: String,
    val baseMaxSpeed: Float,
    var distance: Float = 0f,
    var lateralX: Float = 0f,
    var speed: Float = 0f,
    var lap: Int = 1,
    var finished: Boolean = false,
    var finishTimeMillis: Long = 0L,
    var currentPosition: Int = 6,
    var obstacleSlowdownTime: Float = 0f, // active stun/slow count
    var targetLateralX: Float = 0f,
    var aiSteeringDrift: Float = 0f
)

class RacingEngine(
    val trackSpec: TrackSpec,
    val playerCar: CarSpec
) {
    val racers = mutableListOf<RacerState>()
    val trackObjects = mutableListOf<TrackObject>()
    var raceStartTime: Long = 0L
    var elapsedRaceTimeMillis: Long = 0L
    var isStarted = false
    var countdown = 3.0f // 3 seconds countdown
    var countdownActive = true

    // Player inputs
    var inputSteer = 0f // -1f to 1f
    var inputAccelerate = false
    var inputBrake = false
    var inputNitroActive = false

    // Player specific status
    var playerCoinsCollected = 0
    var playerNitroLevel = 50f // Starts with half nitro tank
    val maxNitroLevel = 100f
    var isPlayerUsingNitroState = false
    var boosterEffectTime = 0f // active booster speed buff timer

    init {
        setupRacers()
        generateTrackObjects()
    }

    private fun setupRacers() {
        racers.clear()
        // Player at bottom starting row
        racers.add(
            RacerState(
                name = "Anda",
                isPlayer = true,
                carColor = playerCar.colorHex,
                baseMaxSpeed = playerCar.getTopSpeedUnits()
            )
        )

        // 5 AI Competitors
        val names = listOf("Neon Falcon", "Shadow Viper", "Slick Cobra", "Apex Avenger", "Zenith Prime")
        val colors = listOf("#FF00FF00", "#FFFFD700", "#FFC000FF", "#FF0088FF", "#FFFF2222")
        val speeds = listOf(
            playerCar.getTopSpeedUnits() * 0.90f,
            playerCar.getTopSpeedUnits() * 0.95f,
            playerCar.getTopSpeedUnits() * 0.98f,
            playerCar.getTopSpeedUnits() * 1.02f,
            playerCar.getTopSpeedUnits() * 1.06f
        )

        for (i in names.indices) {
            racers.add(
                RacerState(
                    name = names[i],
                    isPlayer = false,
                    carColor = colors[i],
                    baseMaxSpeed = speeds[i],
                    distance = -100f * (i + 1), // Grid start staggered behind
                    lateralX = if (i % 2 == 0) -35f else 35f
                )
            )
        }
    }

    private fun generateTrackObjects() {
        trackObjects.clear()
        val interval = 120f
        var dist = 150f

        while (dist < trackSpec.length - 200f) {
            val progressRatio = dist / trackSpec.length
            val curveAtDist = getRoadCurveAt(dist)

            // Spawn Coins
            if (dist % 240f == 0f) {
                // Spawn a line of 3 coins
                val offset = (sin(dist) * 45f).coerceIn(-60f, 60f)
                trackObjects.add(TrackObject(TrackObject.Type.COIN, dist, offset))
                trackObjects.add(TrackObject(TrackObject.Type.COIN, dist + 20f, offset + curveAtDist * 10f))
                trackObjects.add(TrackObject(TrackObject.Type.COIN, dist + 40f, offset + curveAtDist * 20f))
            }

            // Spawn Nitro powerups
            if (dist % 480f == 120f) {
                val offset = ((cos(dist) * 50f) + curveAtDist * 15f).coerceIn(-60f, 60f)
                trackObjects.add(TrackObject(TrackObject.Type.NITRO, dist, offset))
            }

            // Spawn Speed Booster Pads
            if (dist % 600f == 360f) {
                val offset = (curveAtDist * 10f).coerceIn(-40f, 40f)
                trackObjects.add(TrackObject(TrackObject.Type.BOOSTER, dist, offset))
            }

            // Spawn Obstacles (Logs, sand piles, barricades)
            if (trackSpec.obstacleDensity > 0f) {
                if (dist % 320f == 180f && Math.random() < trackSpec.obstacleDensity) {
                    val side = if (sin(dist * 0.5f) > 0f) 50f else -50f
                    val offset = (side - curveAtDist * 10f).coerceIn(-70f, 70f)
                    trackObjects.add(TrackObject(TrackObject.Type.OBSTACLE, dist, offset))
                }
            }

            dist += interval
        }
    }

    // Mathematical curva function for scrolling road representation
    fun getRoadCurveAt(distance: Float): Float {
        // Curve value between -1.2 (sharp left) and 1.2 (sharp right)
        val normalizedDist = distance % trackSpec.length
        return when {
            normalizedDist < 300f -> 0f
            normalizedDist < 800f -> 0.4f * sin((normalizedDist - 300f) * Math.PI.toFloat() / 500f) // Soft right
            normalizedDist < 1200f -> 0f
            normalizedDist < 1800f -> -0.8f * sin((normalizedDist - 1200f) * Math.PI.toFloat() / 600f) // Sharp Left
            normalizedDist < 2100f -> 0.3f * sin((normalizedDist - 1800f) * Math.PI.toFloat() / 150f) // Quick zig-zag
            normalizedDist < 2600f -> 0.9f * sin((normalizedDist - 2100f) * Math.PI.toFloat() / 500f) // Sharp right bend
            else -> 0f
        }
    }

    // Core physics and simulation cycle update, called 60 times/sec (dt = 0.016s)
    fun update(dt: Float, onCrash: () -> Unit, onCoinCollected: () -> Unit, onNitroCollected: () -> Unit) {
        if (countdownActive) {
            countdown -= dt
            if (countdown <= 0f) {
                countdown = 0f
                countdownActive = false
                isStarted = true
                raceStartTime = System.currentTimeMillis()
            }
            return
        }

        if (!isStarted) return
        elapsedRaceTimeMillis = System.currentTimeMillis() - raceStartTime

        // Decay timers
        if (boosterEffectTime > 0f) {
            boosterEffectTime -= dt
        }

        // 1. UPDATE PLAYER PHYSICS
        val player = racers.find { it.isPlayer } ?: return

        if (!player.finished) {
            // Decay slowdowns
            if (player.obstacleSlowdownTime > 0f) {
                player.obstacleSlowdownTime -= dt
            }

            // Target top speed calculation
            var maxSpeed = player.baseMaxSpeed
            val isOffRoad = player.lateralX < -80f || player.lateralX > 80f

            if (isOffRoad) {
                maxSpeed = player.baseMaxSpeed * 0.40f // Mud/grass slow limit (80km/h equivalent)
            } else if (boosterEffectTime > 0f) {
                maxSpeed = player.baseMaxSpeed * 1.50f // Hyper speed boost pads
            }

            // Nitro thrust increase
            val nitroEngaged = inputNitroActive && playerNitroLevel > 0f && inputAccelerate
            isPlayerUsingNitroState = nitroEngaged

            if (nitroEngaged) {
                maxSpeed *= (1f + playerCar.nitroPower * 0.35f)
                playerNitroLevel = (playerNitroLevel - 20f * dt).coerceAtLeast(0f)
            } else {
                // Passively replenish minor nitro
                playerNitroLevel = (playerNitroLevel + 1.5f * dt).coerceAtMost(maxNitroLevel)
            }

            if (player.obstacleSlowdownTime > 0f) {
                maxSpeed *= 0.3f // Sudden log drag
            }

            // Acceleration & Deceleration simulation
            if (inputAccelerate) {
                val accelRate = playerCar.acceleration * (if (nitroEngaged) 22f else 8f) * dt
                player.speed = (player.speed + accelRate).coerceAtMost(maxSpeed)
            } else {
                // Wind resistance friction
                player.speed = (player.speed - 6f * dt).coerceAtLeast(0f)
            }

            if (inputBrake) {
                player.speed = (player.speed - 24f * dt).coerceAtLeast(0f)
            }

            // Horizontal Steering & Drifting Offset
            val roadCurve = getRoadCurveAt(player.distance)
            // Centrifugal drag on road curve pulls player away from center
            val driftFactor = roadCurve * player.speed * 1.3f * dt

            val steerAmount = inputSteer * playerCar.handling * 135f * dt
            player.lateralX += steerAmount - driftFactor
            player.lateralX = player.lateralX.coerceIn(-105f, 105f)

            // Accumulate linear progression
            player.distance += player.speed * 60f * dt

            // Track completion checking
            if (player.distance >= trackSpec.length) {
                if (player.lap < trackSpec.laps) {
                    player.lap++
                    player.distance -= trackSpec.length
                } else {
                    player.finished = true
                    player.distance = trackSpec.length
                    player.speed = 0f
                    player.finishTimeMillis = elapsedRaceTimeMillis
                }
            }

            // Deteksi tabrakan benda di jalan
            checkCollisions(player, onCrash, onCoinCollected, onNitroCollected)
        }

        // 2. UPDATE SMART AI RACERS
        for (ai in racers) {
            if (ai.isPlayer) continue

            if (!ai.finished) {
                if (ai.obstacleSlowdownTime > 0f) {
                    ai.obstacleSlowdownTime -= dt
                }

                // AI Path tracking and steering
                var aiMaxSpeed = ai.baseMaxSpeed
                val roadCurve = getRoadCurveAt(ai.distance)

                // AI wants to track center offset based on its behavior
                // Let's make AI drift somewhat realistic
                ai.aiSteeringDrift += (Math.random().toFloat() * 2f - 1f) * 10f * dt
                ai.aiSteeringDrift = ai.aiSteeringDrift.coerceIn(-20f, 20f)

                // Dynamic target lateral position: stay close to centerline but dodge outer lanes on high curves
                ai.targetLateralX = (-roadCurve * 45f + ai.aiSteeringDrift).coerceIn(-75f, 75f)

                // Steering logic path update
                val steerGap = ai.targetLateralX - ai.lateralX
                val steerStep = 80f * dt
                if (steerGap > 1f) {
                    ai.lateralX = (ai.lateralX + steerStep).coerceAtMost(ai.targetLateralX)
                } else if (steerGap < -1f) {
                    ai.lateralX = (ai.lateralX - steerStep).coerceAtLeast(ai.targetLateralX)
                }

                if (ai.obstacleSlowdownTime > 0f) {
                    aiMaxSpeed *= 0.35f
                }

                // AI acceleration is highly robust and smooth
                if (ai.speed < aiMaxSpeed) {
                    ai.speed = (ai.speed + 6f * dt).coerceAtMost(aiMaxSpeed)
                } else {
                    ai.speed = (ai.speed - 3f * dt).coerceAtLeast(aiMaxSpeed)
                }

                // AI movement linear track updates
                ai.distance += ai.speed * 60f * dt

                if (ai.distance >= trackSpec.length) {
                    if (ai.lap < trackSpec.laps) {
                        ai.lap++
                        ai.distance -= trackSpec.length
                    } else {
                        ai.finished = true
                        ai.distance = trackSpec.length
                        ai.speed = 0f
                        ai.finishTimeMillis = elapsedRaceTimeMillis
                    }
                }
            }
        }

        // 3. REAL-TIME RACING POSITIONS CALCULATION
        val sortedRacers = racers.sortedWith { r1, r2 ->
            // Prioritize status of finish, then laps, then distance progress
            when {
                r1.finished && r2.finished -> r1.finishTimeMillis.compareTo(r2.finishTimeMillis)
                r1.finished -> -1
                r2.finished -> 1
                else -> {
                    val progress1 = (r1.lap - 1) * trackSpec.length + r1.distance
                    val progress2 = (r2.lap - 1) * trackSpec.length + r2.distance
                    progress2.compareTo(progress1) // Descending
                }
            }
        }

        for (i in sortedRacers.indices) {
            sortedRacers[i].currentPosition = i + 1
        }
    }

    private fun checkCollisions(player: RacerState, onCrash: () -> Unit, onCoinCollected: () -> Unit, onNitroCollected: () -> Unit) {
        val grabRangeOffset = 18f // proximity scan distance units
        val grabLateralMargin = 22f // lane margin width

        for (obj in trackObjects) {
            if (!obj.isActive) continue

            // Check if player distance is matching object distance
            val distanceDiff = Math.abs(player.distance - obj.distance)
            if (distanceDiff <= grabRangeOffset) {
                val lateralDiff = Math.abs(player.lateralX - obj.lateralX)
                if (lateralDiff <= grabLateralMargin) {
                    // Trigger collection/collision
                    obj.isActive = false

                    when (obj.type) {
                        TrackObject.Type.COIN -> {
                            playerCoinsCollected += 15 // Bonus koin emas
                            onCoinCollected()
                        }
                        TrackObject.Type.NITRO -> {
                            playerNitroLevel = (playerNitroLevel + 35f).coerceAtMost(maxNitroLevel)
                            onNitroCollected()
                        }
                        TrackObject.Type.BOOSTER -> {
                            boosterEffectTime = 1.8f // Speed buff 1.8 seconds!
                            onNitroCollected() // Plays same whoosh sound
                        }
                        TrackObject.Type.OBSTACLE -> {
                            player.obstacleSlowdownTime = 1.0f // Heavy drop for 1 second
                            player.speed *= 0.25f // Crash speed drop
                            onCrash()
                        }
                    }
                }
            }
        }
    }
}
