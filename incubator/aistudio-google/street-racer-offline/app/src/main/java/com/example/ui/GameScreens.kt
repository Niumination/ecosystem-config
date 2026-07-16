package com.example.ui

import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.*
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.*
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import com.example.data.*
import com.example.game.*
import com.example.ui.components.SynthSoundManager
import kotlin.math.cos
import kotlin.math.sin

@Composable
fun GameAppOrchestrator(viewModel: GameViewModel) {
    val coins by viewModel.coins.collectAsState()
    val ownedCars by viewModel.ownedCars.collectAsState()
    val unlockedTracks by viewModel.unlockedTracks.collectAsState()
    val trackRecords by viewModel.trackRecords.collectAsState()
    val careerLvl by viewModel.careerLevel.collectAsState()

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = Color(0xFF0F172A)
    ) {
        Box(modifier = Modifier.fillMaxSize()) {
            when (viewModel.currentScreen) {
                ScreenState.MAIN_MENU -> MainMenuScreen(viewModel, coins, careerLvl)
                ScreenState.CAREER_OVERVIEW -> CareerOverviewScreen(viewModel, careerLvl)
                ScreenState.CAR_SELECTION -> CarSelectionScreen(viewModel, coins, ownedCars)
                ScreenState.TRACK_SELECTION -> TrackSelectionScreen(viewModel, coins, unlockedTracks, trackRecords)
                ScreenState.PLAYING -> PlayingScreen(viewModel)
                ScreenState.RESULT -> ResultScreen(viewModel)
            }

            // Top right sound toggle (hidden during gameplay)
            if (viewModel.currentScreen != ScreenState.PLAYING) {
                IconButton(
                    onClick = { viewModel.toggleMute() },
                    modifier = Modifier
                        .align(Alignment.TopEnd)
                        .padding(16.dp)
                        .background(Color.Black.copy(alpha = 0.5f), CircleShape)
                ) {
                    Icon(
                        imageVector = if (viewModel.isMuted) Icons.Default.Close else Icons.Default.Check,
                        contentDescription = "Mute",
                        tint = if (viewModel.isMuted) Color.Gray else Color.Yellow
                    )
                }
            }
        }
    }
}

// =========================================================================
// 1. MAIN MENU SCREEN
// =========================================================================
@Composable
fun MainMenuScreen(viewModel: GameViewModel, coins: Int, careerLvl: Int) {
    Box(
        modifier = Modifier.fillMaxSize()
    ) {
        val infiniteTransition = rememberInfiniteTransition(label = "grid")
        val backgroundScroll by infiniteTransition.animateFloat(
            initialValue = 0f,
            targetValue = 1f,
            animationSpec = infiniteRepeatable(
                animation = tween(4000, easing = LinearEasing),
                repeatMode = RepeatMode.Restart
            ),
            label = "grid-scroll"
        )

        Canvas(modifier = Modifier.fillMaxSize()) {
            val w = size.width
            val h = size.height
            // Dark gradient sky
            drawRect(
                brush = Brush.verticalGradient(
                    colors = listOf(Color(0xFF0B0F19), Color(0xFF1E1B4B), Color(0xFF020617))
                )
            )

            // Dynamic grid perspective
            val horizonY = h * 0.45f
            val gridSpacing = 40f
            val offset = backgroundScroll * gridSpacing

            var y = horizonY
            while (y < h) {
                val ratio = (y - horizonY) / (h - horizonY)
                val dynamicY = horizonY + (h - horizonY) * (ratio * ratio)
                drawLine(
                    color = Color(0xFF6366F1).copy(alpha = 0.12f * ratio),
                    start = Offset(0f, dynamicY),
                    end = Offset(w, dynamicY),
                    strokeWidth = 2f
                )
                y += 35f
            }

            val numLines = 14
            for (i in 0..numLines) {
                val startX = w * (i.toFloat() / numLines)
                val targetEnd = w / 2f + (startX - w / 2f) * 4.5f
                drawLine(
                    color = Color(0xFF6366F1).copy(alpha = 0.20f),
                    start = Offset(startX, horizonY),
                    end = Offset(targetEnd, h),
                    strokeWidth = 2f
                )
            }
        }

        // Top Left Gold Star Coins Indicator
        Row(
            modifier = Modifier
                .align(Alignment.TopStart)
                .padding(16.dp)
                .background(Color.Black.copy(alpha = 0.6f), RoundedCornerShape(12.dp))
                .border(1.dp, Color(0xFFFFD700).copy(alpha = 0.4f), RoundedCornerShape(12.dp))
                .padding(horizontal = 14.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(Icons.Default.Star, contentDescription = "Coins", tint = Color(0xFFFFD700), modifier = Modifier.size(18.dp))
            Spacer(modifier = Modifier.width(6.dp))
            Text(text = "$coins COINS", color = Color.White, fontSize = 13.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
        }

        // Tier Career progress tag up top
        Text(
            text = "CAREER LEVEL: $careerLvl",
            modifier = Modifier
                .align(Alignment.TopCenter)
                .padding(top = 22.dp)
                .background(Color(0xFF6366F1).copy(alpha = 0.25f), RoundedCornerShape(8.dp))
                .padding(horizontal = 12.dp, vertical = 6.dp),
            color = Color(0xFF818CF8),
            fontSize = 12.sp,
            fontWeight = FontWeight.Bold,
            fontFamily = FontFamily.Monospace
        )

        // Navigation block
        Column(
            modifier = Modifier
                .fillMaxWidth(0.55f)
                .align(Alignment.CenterStart)
                .padding(start = 48.dp),
            verticalArrangement = Arrangement.Center
        ) {
            Text(
                text = "STREET RACER",
                color = Color.White,
                fontSize = 40.sp,
                fontWeight = FontWeight.Black,
                fontFamily = FontFamily.Monospace,
                lineHeight = 44.sp
            )
            Text(
                text = "OFFLINE RACING ENGINE",
                color = Color(0xFF818CF8),
                fontSize = 12.sp,
                fontWeight = FontWeight.Bold,
                fontFamily = FontFamily.Monospace,
                letterSpacing = 2.sp
            )
            Spacer(modifier = Modifier.height(20.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Button(
                    onClick = {
                        viewModel.playBeepHigh()
                        viewModel.currentScreen = ScreenState.CAREER_OVERVIEW
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF6366F1)),
                    shape = RoundedCornerShape(8.dp),
                    modifier = Modifier.weight(1f).height(46.dp)
                ) {
                    Icon(Icons.Default.Star, contentDescription = "Play", modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("KARIR", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                }

                Button(
                    onClick = {
                        viewModel.playBeepHigh()
                        viewModel.currentGameMode = GameMode.QUICK_RACE
                        viewModel.currentScreen = ScreenState.TRACK_SELECTION
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF3B82F6)),
                    shape = RoundedCornerShape(8.dp),
                    modifier = Modifier.weight(1f).height(46.dp)
                ) {
                    Icon(Icons.Default.PlayArrow, contentDescription = "Quick", modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("QUICK RACE", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Button(
                    onClick = {
                        viewModel.playBeepHigh()
                        viewModel.currentScreen = ScreenState.CAR_SELECTION
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF10B981)),
                    shape = RoundedCornerShape(8.dp),
                    modifier = Modifier.weight(1f).height(44.dp)
                ) {
                    Icon(Icons.Default.Build, contentDescription = "Garage", modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("GARASI", fontWeight = FontWeight.Bold, fontSize = 12.sp)
                }

                Button(
                    onClick = {
                        viewModel.playBeepHigh()
                        viewModel.currentGameMode = GameMode.TIME_TRIAL
                        viewModel.currentScreen = ScreenState.TRACK_SELECTION
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF59E0B)),
                    shape = RoundedCornerShape(8.dp),
                    modifier = Modifier.weight(1f).height(44.dp)
                ) {
                    Text("⏱  TIME TRIAL", fontWeight = FontWeight.Bold, fontSize = 12.sp)
                }
            }
        }

        // Reset game profile option
        Column(
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(24.dp),
            horizontalAlignment = Alignment.End
        ) {
            Text(
                text = "DEVELOPER SPEC : JETPACK COMPOSE NATIVE 60FPS",
                color = Color.White.copy(alpha = 0.35f),
                fontSize = 8.sp,
                fontFamily = FontFamily.Monospace
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = "HAPUS SAVE DATA / RESET PROGRESS",
                color = Color(0xFFEF4444).copy(alpha = 0.8f),
                fontSize = 10.sp,
                fontFamily = FontFamily.Monospace,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.clickable { viewModel.resetSaveData() }
            )
        }
    }
}

// =========================================================================
// 2. CAREER SCREEN
// =========================================================================
@Composable
fun CareerOverviewScreen(viewModel: GameViewModel, careerLvl: Int) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(
                onClick = {
                    viewModel.playBeepLow()
                    viewModel.currentScreen = ScreenState.MAIN_MENU
                },
                modifier = Modifier.background(Color.Black.copy(0.4f), CircleShape)
            ) {
                Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Color.Yellow)
            }
            Text(
                text = "MODE KARIR SEDERHANA",
                color = Color.White,
                fontSize = 24.sp,
                fontWeight = FontWeight.Black,
                fontFamily = FontFamily.Monospace
            )
            Box(Modifier.size(40.dp))
        }

        Spacer(modifier = Modifier.height(16.dp))

        Row(
            modifier = Modifier.fillMaxWidth().weight(1f),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            val levels = listOf(
                Triple(1, "Sunset City Stage", "Target Finis: 3 BESAR\nHadiah Bonus: 100 KOIN\nUnlocks: Emerald Forest Track"),
                Triple(2, "Emerald Forest Stage", "Target Finis: 2 BESAR\nHadiah Bonus: 200 KOIN\nUnlocks: Sahara Dunes Track"),
                Triple(3, "Sahara Dunes Finale", "Target Finis: POSISI 1\nHadiah Bonus: 350 KOIN\nUnlocks: Gelar Champion")
            )

            levels.forEach { (lvlId, title, desc) ->
                val isUnlocked = careerLvl >= lvlId
                val isCurrent = careerLvl == lvlId
                val isCompleted = careerLvl > lvlId

                Card(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxHeight(),
                    colors = CardDefaults.cardColors(
                        containerColor = when {
                            isCurrent -> Color(0xFF1E1B4B)
                            isCompleted -> Color(0xFF0F172A)
                            else -> Color(0xFF020617).copy(alpha = 0.5f)
                        }
                    ),
                    shape = RoundedCornerShape(12.dp),
                    border = BorderStroke(
                        width = if (isCurrent) 2.dp else 1.dp,
                        color = when {
                            isCurrent -> Color(0xFF6366F1)
                            isCompleted -> Color(0xFF10B981)
                            else -> Color.White.copy(alpha = 0.08f)
                        }
                    )
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(16.dp),
                        verticalArrangement = Arrangement.SpaceBetween
                    ) {
                        Column {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = "STAGE 0$lvlId",
                                    color = if (isUnlocked) Color(0xFF818CF8) else Color.Gray,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    fontFamily = FontFamily.Monospace
                                )
                                Icon(
                                    imageVector = when {
                                        isCompleted -> Icons.Default.CheckCircle
                                        isCurrent -> Icons.Default.Star
                                        else -> Icons.Default.Lock
                                    },
                                    contentDescription = "Status",
                                    tint = when {
                                        isCompleted -> Color(0xFF10B981)
                                        isCurrent -> Color(0xFFF59E0B)
                                        else -> Color.Gray
                                    },
                                    modifier = Modifier.size(20.dp)
                                )
                            }
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = title,
                                color = if (isUnlocked) Color.White else Color.Gray,
                                fontSize = 16.sp,
                                fontWeight = FontWeight.Bold,
                                fontFamily = FontFamily.Monospace
                            )
                            Spacer(modifier = Modifier.height(12.dp))
                            Text(
                                text = desc,
                                color = if (isUnlocked) Color(0xFFCBD5E1) else Color.Gray.copy(alpha = 0.6f),
                                fontSize = 11.sp,
                                lineHeight = 16.sp,
                                fontFamily = FontFamily.Monospace
                            )
                        }

                        if (isCurrent) {
                            Button(
                                onClick = {
                                    viewModel.playBeepHigh()
                                    viewModel.currentGameMode = GameMode.CAREER
                                    viewModel.selectedTrackId = when(lvlId) {
                                        1 -> "track_city"
                                        2 -> "track_forest"
                                        else -> "track_desert"
                                    }
                                    viewModel.startNewRace()
                                },
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF6366F1)),
                                shape = RoundedCornerShape(6.dp),
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                Text("MULAI BALAPAN", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            }
                        } else if (isUnlocked && isCompleted) {
                            Button(
                                onClick = {
                                    viewModel.playBeepHigh()
                                    viewModel.currentGameMode = GameMode.CAREER
                                    viewModel.selectedTrackId = when(lvlId) {
                                        1 -> "track_city"
                                        2 -> "track_forest"
                                        else -> "track_desert"
                                    }
                                    viewModel.startNewRace()
                                },
                                colors = ButtonDefaults.buttonColors(containerColor = Color.DarkGray),
                                shape = RoundedCornerShape(6.dp),
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                Text("REPLAY BALAPAN", fontSize = 12.sp, color = Color.White)
                            }
                        } else {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(36.dp)
                                    .background(Color.Black.copy(0.1f), RoundedCornerShape(6.dp)),
                                contentAlignment = Alignment.Center
                            ) {
                                Text("TERKUNCI", color = Color.Gray, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
                            }
                        }
                    }
                }
            }
        }
    }
}

// =========================================================================
// 3. GARAGE / CAR SELECTION SCREEN
// =========================================================================
@Composable
fun CarSelectionScreen(viewModel: GameViewModel, coins: Int, ownedCars: Set<String>) {
    var specIndex by remember { mutableStateOf(0) }
    val activeCar = viewModel.CAR_LIST[specIndex]
    val isOwned = ownedCars.contains(activeCar.id)
    val isSelected = viewModel.selectedCarId == activeCar.id

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(
                onClick = {
                    viewModel.playBeepLow()
                    viewModel.currentScreen = ScreenState.MAIN_MENU
                },
                modifier = Modifier.background(Color.Black.copy(0.4f), CircleShape)
            ) {
                Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Color.Yellow)
            }
            Text(
                text = "GARASI SHOWROOM MOBIL",
                color = Color.White,
                fontSize = 22.sp,
                fontWeight = FontWeight.Bold,
                fontFamily = FontFamily.Monospace
            )
            Row(
                modifier = Modifier
                    .background(Color.Black.copy(alpha = 0.5f), RoundedCornerShape(8.dp))
                    .padding(horizontal = 10.dp, vertical = 6.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(Icons.Default.Star, contentDescription = "Coins", tint = Color(0xFFFFD700), modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(4.dp))
                Text(text = "$coins COINS", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        Row(
            modifier = Modifier.fillMaxWidth().weight(1f),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Left list selectors
            Column(
                modifier = Modifier
                    .weight(0.45f)
                    .fillMaxHeight(),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                viewModel.CAR_LIST.forEachIndexed { idx, car ->
                    val carSelected = idx == specIndex
                    val carOwned = ownedCars.contains(car.id)
                    val carCurrent = viewModel.selectedCarId == car.id

                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .weight(1f)
                            .clickable {
                                viewModel.playBeepLow()
                                specIndex = idx
                            },
                        colors = CardDefaults.cardColors(
                            containerColor = if (carSelected) Color(0xFF1E1B4B) else Color(0xFF020617).copy(alpha = 0.6f)
                        ),
                        border = BorderStroke(
                            width = 1.5.dp,
                            color = if (carSelected) Color(0xFF3333D7) else if (carCurrent) Color(0xFF10B981) else Color.Transparent
                        )
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxSize()
                                .padding(horizontal = 12.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(
                                    modifier = Modifier
                                        .size(16.dp)
                                        .clip(CircleShape)
                                        .background(Color(android.graphics.Color.parseColor(car.colorHex)))
                                )
                                Spacer(modifier = Modifier.width(10.dp))
                                Text(
                                    text = car.name,
                                    color = if (carSelected) Color.White else Color.Gray,
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.Bold,
                                    fontFamily = FontFamily.Monospace
                                )
                            }
                            if (carCurrent) {
                                Icon(Icons.Default.PlayArrow, contentDescription = "Active", tint = Color(0xFF10B981), modifier = Modifier.size(16.dp))
                            } else if (!carOwned) {
                                Icon(Icons.Default.Lock, contentDescription = "Locked", tint = Color.Gray, modifier = Modifier.size(14.dp))
                            }
                        }
                    }
                }
            }

            // Right side Showcase
            Card(
                modifier = Modifier
                    .weight(0.55f)
                    .fillMaxHeight(),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF0F172A)),
                border = BorderStroke(1.dp, Color.White.copy(0.08f))
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(16.dp),
                    verticalArrangement = Arrangement.SpaceBetween
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .weight(0.40f)
                            .clip(RoundedCornerShape(8.dp))
                            .background(Color.Black.copy(0.3f)),
                        contentAlignment = Alignment.Center
                    ) {
                        val infiniteOffset = rememberInfiniteTransition(label = "flame")
                        val fl by infiniteOffset.animateFloat(
                            initialValue = 0.9f,
                            targetValue = 1.4f,
                            animationSpec = infiniteRepeatable(
                                animation = tween(150, easing = FastOutSlowInEasing),
                                repeatMode = RepeatMode.Reverse
                            ), label = "fire"
                        )
                        Canvas(modifier = Modifier.fillMaxSize().padding(12.dp)) {
                            val w = size.width
                            val h = size.height
                            val midX = w / 2f
                            val midY = h / 2f
                            val carCol = Color(android.graphics.Color.parseColor(activeCar.colorHex))

                            val spoilerWidth = 135f
                            val spoilerHeight = 10f
                            val spoilerY = midY - 24f
                            drawRect(
                                color = carCol.copy(alpha = 0.8f),
                                topLeft = Offset(midX - spoilerWidth / 2f, spoilerY),
                                size = Size(spoilerWidth, spoilerHeight)
                            )
                            drawRect(color = Color.Black, topLeft = Offset(midX - 40f, spoilerY + 10f), size = Size(8f, 14f))
                            drawRect(color = Color.Black, topLeft = Offset(midX + 32f, spoilerY + 10f), size = Size(8f, 14f))

                            val bodyW = 105f
                            val bodyH = 46f
                            val bodyY = midY - 6f
                            drawRoundRect(
                                color = carCol,
                                topLeft = Offset(midX - bodyW / 2f, bodyY),
                                size = Size(bodyW, bodyH),
                                cornerRadius = CornerRadius(6f, 6f)
                            )

                            val rWinW = 80f
                            val rWinH = 20f
                            drawRoundRect(
                                color = Color(0xFF64748B),
                                topLeft = Offset(midX - rWinW / 2f, bodyY + 3f),
                                size = Size(rWinW, rWinH),
                                cornerRadius = CornerRadius(4f, 4f)
                            )

                            drawRoundRect(color = Color.Black, topLeft = Offset(midX - bodyW / 2f - 12f, bodyY + 12f), size = Size(14f, 28f), cornerRadius = CornerRadius(4f, 4f))
                            drawRoundRect(color = Color.Black, topLeft = Offset(midX + bodyW / 2f - 2f, bodyY + 12f), size = Size(14f, 28f), cornerRadius = CornerRadius(4f, 4f))

                            drawRect(color = Color(0xFFEF4444), topLeft = Offset(midX - bodyW / 2f + 4f, bodyY + 28f), size = Size(18f, 6f))
                            drawRect(color = Color(0xFFEF4444), topLeft = Offset(midX + bodyW / 2f - 22f, bodyY + 28f), size = Size(18f, 6f))

                            val exL1 = bodyY + 40f
                            drawCircle(color = Color(0xFFFF9F43).copy(alpha = 0.8f), center = Offset(midX - 30f, exL1 + 6f), radius = 5f * fl)
                            drawCircle(color = Color(0xFFFF9F43).copy(alpha = 0.8f), center = Offset(midX + 30f, exL1 + 6f), radius = 5f * fl)
                        }
                    }

                    Column(modifier = Modifier.weight(0.60f).padding(top = 8.dp)) {
                        Text(text = activeCar.name, color = Color.White, fontWeight = FontWeight.Bold, fontSize = 16.sp, fontFamily = FontFamily.Monospace)
                        Spacer(modifier = Modifier.height(4.dp))

                        val stats = listOf(
                            "TOP SPEED" to activeCar.topSpeedKmh / 350f,
                            "ACCELERATION" to activeCar.acceleration / 2f,
                            "HANDLING" to activeCar.handling / 2.0f,
                            "NITRO BURN" to activeCar.nitroPower / 2.0f
                        )

                        stats.forEach { (label, ratio) ->
                            Column(modifier = Modifier.padding(bottom = 5.dp)) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween
                                ) {
                                    Text(label, color = Color.Gray, fontSize = 9.sp, fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold)
                                    val actVal = when (label) {
                                        "TOP SPEED" -> "${activeCar.topSpeedKmh.toInt()} KMH"
                                        "ACCELERATION" -> "${(activeCar.acceleration * 10f).toInt()} PNT"
                                        "HANDLING" -> "${(activeCar.handling * 100f).toInt()}%"
                                        else -> "${(activeCar.nitroPower * 100f).toInt()}%"
                                    }
                                    Text(actVal, color = Color.White, fontSize = 9.sp, fontFamily = FontFamily.Monospace)
                                }
                                LinearProgressIndicator(
                                    progress = { ratio.coerceIn(0f, 1f) },
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(4.dp)
                                        .clip(CircleShape),
                                    color = Color(0xFF6366F1),
                                    trackColor = Color.DarkGray
                                )
                            }
                        }

                        Spacer(modifier = Modifier.height(6.dp))

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            if (isSelected) {
                                Button(
                                    onClick = {},
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF10B981)),
                                    enabled = false,
                                    shape = RoundedCornerShape(6.dp),
                                    modifier = Modifier.weight(1f)
                                ) {
                                    Text("TERPILIH UNTUK MAIN", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                                }
                            } else if (isOwned) {
                                Button(
                                    onClick = {
                                        viewModel.playBeepHigh()
                                        viewModel.selectCar(activeCar.id)
                                    },
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF3B82F6)),
                                    shape = RoundedCornerShape(6.dp),
                                    modifier = Modifier.weight(1f)
                                ) {
                                    Text("PILIH MOBIL INI", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                                }
                            } else {
                                Button(
                                    onClick = { viewModel.buyCar(activeCar) },
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF59E0B)),
                                    enabled = coins >= activeCar.price,
                                    shape = RoundedCornerShape(6.dp),
                                    modifier = Modifier.weight(1f)
                                ) {
                                    Text("BELI (${activeCar.price} KOIN)", color = Color.Black, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

// =========================================================================
// 4. MAPS / TRACK SELECTION SCREEN
// =========================================================================
@Composable
fun TrackSelectionScreen(viewModel: GameViewModel, coins: Int, unlockedTracks: Set<String>, records: Map<String, TrackRecord>) {
    var tIdx by remember { mutableStateOf(0) }
    val track = viewModel.TRACK_LIST[tIdx]
    val isUnlocked = unlockedTracks.contains(track.id)
    val priceToUnlock = when(track.id) {
        "track_forest" -> 150
        "track_desert" -> 350
        else -> 0
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(
                onClick = {
                    viewModel.playBeepLow()
                    viewModel.currentScreen = ScreenState.MAIN_MENU
                },
                modifier = Modifier.background(Color.Black.copy(0.4f), CircleShape)
            ) {
                Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Color.Yellow)
            }
            Text(
                text = "PILIH CIRKUIT : ${viewModel.currentGameMode}",
                color = Color.White,
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold,
                fontFamily = FontFamily.Monospace
            )
            Row(
                modifier = Modifier
                    .background(Color.Black.copy(alpha = 0.5f), RoundedCornerShape(8.dp))
                    .padding(horizontal = 10.dp, vertical = 6.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(Icons.Default.Star, contentDescription = "Coins", tint = Color(0xFFFFD700), modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(4.dp))
                Text(text = "$coins COINS", color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        Row(
            modifier = Modifier.fillMaxWidth().weight(1f),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Column(
                modifier = Modifier
                    .weight(0.45f)
                    .fillMaxHeight(),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                viewModel.TRACK_LIST.forEachIndexed { idx, t ->
                    val isSel = idx == tIdx
                    val hasUnlocked = unlockedTracks.contains(t.id)

                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .weight(1f)
                            .clickable {
                                viewModel.playBeepLow()
                                tIdx = idx
                            },
                        colors = CardDefaults.cardColors(
                            containerColor = if (isSel) Color(0xFF1E1B4B) else Color(0xFF020617).copy(alpha = 0.6f)
                        ),
                        border = BorderStroke(1.5.dp, if (isSel) Color(0xFF6366F1) else Color.Transparent)
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxSize()
                                .padding(horizontal = 12.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Column(verticalArrangement = Arrangement.Center) {
                                Text(t.name, color = if (isSel) Color.White else Color.Gray, fontSize = 13.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
                                Text("${t.length.toInt()} Meters", color = Color.Gray, fontSize = 10.sp)
                            }
                            if (!hasUnlocked) {
                                Icon(Icons.Default.Lock, contentDescription = "Locked", tint = Color.Gray, modifier = Modifier.size(14.dp))
                            }
                        }
                    }
                }
            }

            Card(
                modifier = Modifier
                    .weight(0.55f)
                    .fillMaxHeight(),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF0F172A)),
                border = BorderStroke(1.dp, Color.White.copy(0.08f))
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(16.dp),
                    verticalArrangement = Arrangement.SpaceBetween
                ) {
                    Column {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text(track.name, color = Color.White, fontWeight = FontWeight.Bold, fontSize = 18.sp, fontFamily = FontFamily.Monospace)
                            Box(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(4.dp))
                                    .background(if (isUnlocked) Color(0xFF10B981) else Color(0xFFEF4444))
                                    .padding(horizontal = 6.dp, vertical = 2.dp)
                            ) {
                                Text(
                                    text = if (isUnlocked) "TIER UNLOCKED" else "TERKUNCI",
                                    color = Color.White,
                                    fontSize = 8.sp,
                                    fontWeight = FontWeight.Bold,
                                    fontFamily = FontFamily.Monospace
                                )
                            }
                        }
                        Spacer(modifier = Modifier.height(10.dp))
                        Text(track.description, color = Color(0xFFCBD5E1), fontSize = 11.sp, fontFamily = FontFamily.Monospace, lineHeight = 16.sp)

                        Spacer(modifier = Modifier.height(14.dp))
                        val record = records[track.id]
                        if (record != null) {
                            val totalMs = record.bestTimeMillis
                            val minutes = (totalMs / 60000).toInt()
                            val seconds = ((totalMs % 60000) / 1000).toInt()
                            val tenths = ((totalMs % 1000) / 100).toInt()
                            val formattedTime = String.format("%02d:%02d.%01d", minutes, seconds, tenths)

                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                Text("REKOR TERBAIK WAKTU:", color = Color.Gray, fontSize = 10.sp, fontFamily = FontFamily.Monospace)
                                Text(formattedTime, color = Color.Yellow, fontSize = 10.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
                            }
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                Text("POSISI FINISH TERTINGGI:", color = Color.Gray, fontSize = 10.sp, fontFamily = FontFamily.Monospace)
                                Text("${record.highPosition}st Place", color = Color(0xFF10B981), fontSize = 10.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
                            }
                        } else {
                            Text("REKOR : BELUM PERNAH BALAPAN", color = Color.Gray, fontSize = 10.sp, fontFamily = FontFamily.Monospace)
                        }
                    }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        if (isUnlocked) {
                            Button(
                                onClick = {
                                    viewModel.playBeepHigh()
                                    viewModel.selectedTrackId = track.id
                                    viewModel.startNewRace()
                                },
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF6366F1)),
                                shape = RoundedCornerShape(6.dp),
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                Text("GAS MULAI BALAP", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            }
                        } else {
                            Button(
                                onClick = { viewModel.buyTrack(track, priceToUnlock) },
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF59E0B)),
                                enabled = coins >= priceToUnlock,
                                shape = RoundedCornerShape(6.dp),
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                Icon(Icons.Default.Lock, contentDescription = "Buy", modifier = Modifier.size(16.dp))
                                Spacer(modifier = Modifier.width(6.dp))
                                Text("UNLOCK DENGAN ${priceToUnlock} KOIN", color = Color.Black, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }
        }
    }
}

// =========================================================================
// 5. THE GAMEPLAY SCREEN & CUSTOM RENDER CANVAS ENGINE (60FPS LOOP)
// =========================================================================
@Composable
fun PlayingScreen(viewModel: GameViewModel) {
    val engine = viewModel.activeEngine ?: return
    val playerCar = viewModel.CAR_LIST.find { it.id == viewModel.selectedCarId } ?: viewModel.CAR_LIST[0]
    val isPaused = viewModel.isPaused

    LaunchedEffect(engine, isPaused) {
        if (isPaused) return@LaunchedEffect
        var lastTime = System.nanoTime()
        while (isActive) {
            withFrameMillis { _ ->
                val now = System.nanoTime()
                val dt = ((now - lastTime) / 1_000_000_000f).coerceIn(0.005f, 0.05f)
                lastTime = now

                engine.update(dt,
                    onCrash = {
                        viewModel.soundManager.playCrashSound()
                    },
                    onCoinCollected = {
                        viewModel.soundManager.playCoinSound()
                    },
                    onNitroCollected = {
                        viewModel.soundManager.playNitroSound()
                    }
                )

                val p = engine.racers.find { it.isPlayer }
                p?.let {
                    val ratio = (it.speed / p.baseMaxSpeed).coerceIn(0f, 1f)
                    viewModel.soundManager.updateEnginePitch(ratio)
                }

                if (p?.finished == true) {
                    viewModel.completeRaceSimulation(engine)
                }
            }
            delay(16)
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black)
    ) {
        // Pseudo-3D Raster Scrolling custom canvas drawing
        Canvas(
            modifier = Modifier.fillMaxSize()
        ) {
            val w = size.width
            val h = size.height
            val skyCol = Color(android.graphics.Color.parseColor(engine.trackSpec.skyColor))
            val grassCol = Color(android.graphics.Color.parseColor(engine.trackSpec.grassColor))
            val roadCol = Color(android.graphics.Color.parseColor(engine.trackSpec.roadColor))

            // 1. SKY
            val horizonY = h * 0.40f
            drawRect(
                brush = Brush.verticalGradient(
                    colors = listOf(skyCol, skyCol.copy(alpha = 0.5f), Color(0xFFFF9F43).copy(alpha = 0.2f)),
                    startY = 0f,
                    endY = horizonY
                ),
                topLeft = Offset(0f, 0f),
                size = Size(w, horizonY)
            )

            // Sun / star flare
            drawCircle(
                color = Color(0xFFFF9F43).copy(alpha = 0.4f),
                radius = 65f,
                center = Offset(w / 2f, horizonY - 12f)
            )

            // 2. RECEDING SECTORS GROUND & ROAD
            val player = engine.racers.find { it.isPlayer } ?: return@Canvas
            val viewDistanceScope = 380f
            val segmentsStep = 18

            var prevScreenL = 0f
            var prevScreenR = 0f
            var prevScreenY = h

            for (i in segmentsStep downTo 1) {
                val ratio = i.toFloat() / segmentsStep
                val targetDistance = player.distance + (ratio * viewDistanceScope)
                val screenY = horizonY + (h - horizonY) * (1f - ratio) * (1f - ratio)

                val curveAtPoint = engine.getRoadCurveAt(targetDistance)
                val cumulativeDrift = curveAtPoint * 125f * (1f - ratio)

                val centerScreenX = w / 2f + cumulativeDrift
                val baseWidth = w * 0.55f
                val roadWidth = baseWidth * (1f - ratio) * (1f - ratio)

                val screenL = centerScreenX - roadWidth / 2f
                val screenR = centerScreenX + roadWidth / 2f

                val stepIdx = (targetDistance / 40f).toInt()
                val isStripeLight = stepIdx % 2 == 0

                val currentGrassColor = if (isStripeLight) grassCol else grassCol.copy(red = (grassCol.red * 0.82f).coerceIn(0f, 1f))
                val currentRoadColor = if (isStripeLight) roadCol else roadCol.copy(red = (roadCol.red * 1.08f).coerceIn(0f, 1f))

                // Draw grass ground trapezoid
                val grassPath = Path().apply {
                    moveTo(0f, prevScreenY)
                    lineTo(w, prevScreenY)
                    lineTo(w, screenY)
                    lineTo(0f, screenY)
                    close()
                }
                drawPath(grassPath, color = currentGrassColor)

                // Draw asphalt road polygon
                if (i < segmentsStep) {
                    val roadPath = Path().apply {
                        moveTo(prevScreenL, prevScreenY)
                        lineTo(prevScreenR, prevScreenY)
                        lineTo(screenR, screenY)
                        lineTo(screenL, screenY)
                        close()
                    }
                    drawPath(roadPath, color = currentRoadColor)

                    // Draw outer side rumble lines (red & white steps)
                    val stripW = 14f * (1f - ratio)
                    val outerBorderCol = if (isStripeLight) Color(0xFFEF4444) else Color.White

                    val leftStrip = Path().apply {
                        moveTo(prevScreenL - stripW, prevScreenY)
                        lineTo(prevScreenL, prevScreenY)
                        lineTo(screenL, screenY)
                        lineTo(screenL - stripW, screenY)
                        close()
                    }
                    drawPath(leftStrip, color = outerBorderCol)

                    val rightStrip = Path().apply {
                        moveTo(prevScreenR, prevScreenY)
                        lineTo(prevScreenR + stripW, prevScreenY)
                        lineTo(screenR + stripW, screenY)
                        lineTo(screenR, screenY)
                        close()
                    }
                    drawPath(rightStrip, color = outerBorderCol)

                    // Center dash divider lines
                    if (isStripeLight) {
                        val dashW = 5f * (1f - ratio)
                        val cenXPrev = (prevScreenL + prevScreenR) / 2f
                        val cenXCurr = (screenL + screenR) / 2f
                        val centerDashPath = Path().apply {
                            moveTo(cenXPrev - dashW / 2f, prevScreenY)
                            lineTo(cenXPrev + dashW / 2f, prevScreenY)
                            lineTo(cenXCurr + dashW / 2f, screenY)
                            lineTo(cenXCurr - dashW / 2f, screenY)
                            close()
                        }
                        drawPath(centerDashPath, color = Color.White)
                    }
                }

                prevScreenL = screenL
                prevScreenR = screenR
                prevScreenY = screenY
            }

            // 3. DRAW POWERUPS AND ROADWAY COINS
            engine.trackObjects.forEach { obj ->
                val distDiff = obj.distance - player.distance
                if (distDiff in 0f..viewDistanceScope && obj.isActive) {
                    val layerRatio = distDiff / viewDistanceScope
                    val layerScreenY = horizonY + (h - horizonY) * (1f - layerRatio) * (1f - layerRatio)

                    val curve = engine.getRoadCurveAt(obj.distance)
                    val centerRoadX = w / 2f + (curve * 125f * (1f - layerRatio))
                    val roadW = (w * 0.55f) * (1f - layerRatio) * (1f - layerRatio)

                    val entityX = centerRoadX + (obj.lateralX * roadW / 180f)
                    val sizeScale = 45f * (1f - layerRatio)

                    if (sizeScale > 1f) {
                        when (obj.type) {
                            TrackObject.Type.COIN -> {
                                drawCircle(
                                    color = Color(0xFFFFD700),
                                    radius = sizeScale * 0.44f,
                                    center = Offset(entityX, layerScreenY - 10f)
                                )
                                drawCircle(
                                    color = Color(0xFFF59E0B),
                                    radius = sizeScale * 0.34f,
                                    center = Offset(entityX, layerScreenY - 10f)
                                )
                                drawCircle(
                                    color = Color.White,
                                    radius = sizeScale * 0.12f,
                                    center = Offset(entityX - sizeScale * 0.1f, layerScreenY - 12f)
                                )
                            }
                            TrackObject.Type.NITRO -> {
                                val rectSize = sizeScale * 0.65f
                                drawRoundRect(
                                    color = Color(0xFF00E1FF),
                                    topLeft = Offset(entityX - rectSize / 2f, layerScreenY - rectSize * 1.4f - 10f),
                                    size = Size(rectSize, rectSize * 1.4f),
                                    cornerRadius = CornerRadius(rectSize * 0.3f, rectSize * 0.3f)
                                )
                                drawCircle(
                                    color = Color.White,
                                    radius = rectSize * 0.18f,
                                    center = Offset(entityX, layerScreenY - rectSize * 0.6f - 10f)
                                )
                            }
                            TrackObject.Type.BOOSTER -> {
                                val arrowW = roadW * 0.38f
                                val arrowPath = Path().apply {
                                    moveTo(entityX - arrowW / 2f, layerScreenY)
                                    lineTo(entityX + arrowW / 2f, layerScreenY)
                                    lineTo(entityX, layerScreenY - sizeScale * 0.52f)
                                    close()
                                }
                                drawPath(arrowPath, color = Color(0xFFF59E0B))
                            }
                            TrackObject.Type.OBSTACLE -> {
                                val logW = sizeScale * 1.4f
                                val logH = sizeScale * 0.55f
                                drawRoundRect(
                                    color = Color(0xFF78350F),
                                    topLeft = Offset(entityX - logW / 2f, layerScreenY - logH),
                                    size = Size(logW, logH),
                                    cornerRadius = CornerRadius(3f, 3f)
                                )
                                drawRect(
                                    color = Color(0xFF451A03),
                                    topLeft = Offset(entityX - logW / 4f, layerScreenY - logH + 2f),
                                    size = Size(logW / 2f, logH - 4f)
                                )
                            }
                        }
                    }
                }
            }

            // 4. DRAW Smart AI CAR COMPETITORS
            engine.racers.forEach { ai ->
                if (ai.isPlayer) return@forEach

                val distDiff = ai.distance - player.distance
                if (distDiff in -50f..viewDistanceScope && !ai.finished) {
                    val layerRatio = (distDiff / viewDistanceScope).coerceIn(0f, 1f)
                    val layerScreenY = horizonY + (h - horizonY) * (1f - layerRatio) * (1f - layerRatio)

                    val curve = engine.getRoadCurveAt(ai.distance)
                    val centerRoadX = w / 2f + (curve * 125f * (1f - layerRatio))
                    val roadW = (w * 0.55f) * (1f - layerRatio) * (1f - layerRatio)

                    val racerX = centerRoadX + (ai.lateralX * roadW / 180f)
                    val carScale = 65f * (1f - layerRatio)

                    if (carScale > 2f) {
                        val col = Color(android.graphics.Color.parseColor(ai.carColor))
                        // AI Base Chassis
                        drawRect(
                            color = col,
                            topLeft = Offset(racerX - carScale / 2f, layerScreenY - carScale * 0.5f),
                            size = Size(carScale, carScale * 0.45f)
                        )
                        // Rear windshield
                        drawRect(
                            color = Color(0xFF1E293B),
                            topLeft = Offset(racerX - carScale * 0.35f, layerScreenY - carScale * 0.45f),
                            size = Size(carScale * 0.7f, carScale * 0.15f)
                        )
                        // taillights
                        drawRect(
                            color = Color.Red,
                            topLeft = Offset(racerX - carScale * 0.45f, layerScreenY - carScale * 0.22f),
                            size = Size(carScale * 0.16f, carScale * 0.08f)
                        )
                        drawRect(
                            color = Color.Red,
                            topLeft = Offset(racerX + carScale * 0.29f, layerScreenY - carScale * 0.22f),
                            size = Size(carScale * 0.16f, carScale * 0.08f)
                        )
                        // tyres
                        drawRect(color = Color.Black, topLeft = Offset(racerX - carScale * 0.48f, layerScreenY - carScale * 0.12f), size = Size(carScale * 0.14f, carScale * 0.16f))
                        drawRect(color = Color.Black, topLeft = Offset(racerX + carScale * 0.34f, layerScreenY - carScale * 0.12f), size = Size(carScale * 0.14f, carScale * 0.16f))
                    }
                }
            }

            // 5. DRAW PLAYER CAR IN FOREGROUND
            val playerScale = 140f
            val centerRoadForeground = w / 2f
            val playerCanvasX = centerRoadForeground + (player.lateralX * w * 0.55f / 180f)
            val pCarY = h * 0.78f

            val baseCol = Color(android.graphics.Color.parseColor(playerCar.colorHex))
            val bankAngleDegrees = engine.inputSteer * 7f

            withTransform({
                rotate(degrees = bankAngleDegrees, pivot = Offset(playerCanvasX, pCarY + playerScale * 0.2f))
            }) {
                // Tyres
                drawRoundRect(
                    color = Color.Black,
                    topLeft = Offset(playerCanvasX - playerScale * 0.48f, pCarY + playerScale * 0.15f),
                    size = Size(25f, 52f),
                    cornerRadius = CornerRadius(6f, 6f)
                )
                drawRoundRect(
                    color = Color.Black,
                    topLeft = Offset(playerCanvasX + playerScale * 0.31f, pCarY + playerScale * 0.15f),
                    size = Size(25f, 52f),
                    cornerRadius = CornerRadius(6f, 6f)
                )

                // Spoiler
                drawRect(
                    color = baseCol.copy(alpha = 0.9f),
                    topLeft = Offset(playerCanvasX - playerScale * 0.55f, pCarY - 18f),
                    size = Size(playerScale * 1.1f, 15f)
                )
                drawRect(color = Color.Black, topLeft = Offset(playerCanvasX - 35f, pCarY - 3f), size = Size(8f, 12f))
                drawRect(color = Color.Black, topLeft = Offset(playerCanvasX + 27f, pCarY - 3f), size = Size(8f, 12f))

                // Frame Chassis Cabin
                drawRoundRect(
                    color = baseCol,
                    topLeft = Offset(playerCanvasX - playerScale * 0.4f, pCarY + 6f),
                    size = Size(playerScale * 0.8f, playerScale * 0.45f),
                    cornerRadius = CornerRadius(10f, 10f)
                )

                // Rear windshield
                drawRoundRect(
                    color = Color(0xFF64748B),
                    topLeft = Offset(playerCanvasX - playerScale * 0.31f, pCarY + 12f),
                    size = Size(playerScale * 0.62f, 22f),
                    cornerRadius = CornerRadius(6f, 6f)
                )

                // Red Braking Taillights
                val tailLightColor = if (engine.inputBrake) Color(0xFFFF2222) else Color(0x99FF0000)
                drawRect(color = tailLightColor, topLeft = Offset(playerCanvasX - playerScale * 0.36f, pCarY + 44f), size = Size(26f, 10f))
                drawRect(color = tailLightColor, topLeft = Offset(playerCanvasX + playerScale * 0.18f, pCarY + 44f), size = Size(26f, 10f))

                // Exhaust Nitro fire effects!
                if (engine.isPlayerUsingNitroState) {
                    val fireWidth = 24f
                    val fireHeight = 44f
                    drawRoundRect(
                        color = Color(0xFF00E1FF),
                        topLeft = Offset(playerCanvasX - 45f, pCarY + playerScale * 0.45f),
                        size = Size(fireWidth, fireHeight),
                        cornerRadius = CornerRadius(6f, 6f)
                    )
                    drawRoundRect(
                        color = Color.White,
                        topLeft = Offset(playerCanvasX - 41f, pCarY + playerScale * 0.45f + 8f),
                        size = Size(16f, fireHeight * 0.5f),
                        cornerRadius = CornerRadius(4f, 4f)
                    )

                    drawRoundRect(
                        color = Color(0xFF00E1FF),
                        topLeft = Offset(playerCanvasX + 21f, pCarY + playerScale * 0.45f),
                        size = Size(fireWidth, fireHeight),
                        cornerRadius = CornerRadius(6f, 6f)
                    )
                    drawRoundRect(
                        color = Color.White,
                        topLeft = Offset(playerCanvasX + 25f, pCarY + playerScale * 0.45f + 8f),
                        size = Size(16f, fireHeight * 0.5f),
                        cornerRadius = CornerRadius(4f, 4f)
                    )
                }
            }
        }

        // 6. HUD DISPLAY DATAPANEL
        Column(
            modifier = Modifier
                .align(Alignment.TopCenter)
                .padding(12.dp)
                .fillMaxWidth(0.6f)
                .clip(RoundedCornerShape(10.dp))
                .background(Color.Black.copy(0.5f))
                .border(0.5.dp, Color.White.copy(0.15f), RoundedCornerShape(10.dp))
                .padding(vertical = 6.dp, horizontal = 12.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                val kmhSpeed = (engine.racers.find { it.isPlayer }?.speed ?: 0f) * 320f / engine.playerCar.getTopSpeedUnits()
                Column(horizontalAlignment = Alignment.Start) {
                    Text("SPEED", color = Color.Gray, fontSize = 7.sp, fontFamily = FontFamily.Monospace)
                    Text("${kmhSpeed.toInt()} KM/H", color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
                }

                val pRank = engine.racers.find { it.isPlayer }?.currentPosition ?: 6
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("POSITION", color = Color.Gray, fontSize = 7.sp, fontFamily = FontFamily.Monospace)
                    Text("$pRank / 6", color = Color.Yellow, fontSize = 15.sp, fontWeight = FontWeight.Black, fontFamily = FontFamily.Monospace)
                }

                val pLap = engine.racers.find { it.isPlayer }?.lap ?: 1
                Column(horizontalAlignment = Alignment.End) {
                    Text("LAP SISA", color = Color.Gray, fontSize = 7.sp, fontFamily = FontFamily.Monospace)
                    Text("$pLap / ${engine.trackSpec.laps}", color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
                }
            }

            Spacer(modifier = Modifier.height(4.dp))

            val currentLvlDistance = engine.racers.find { it.isPlayer }?.distance ?: 0f
            val completionRatio = (currentLvlDistance / engine.trackSpec.length).coerceIn(0f, 1f)
            LinearProgressIndicator(
                progress = { completionRatio },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(3.dp)
                    .clip(CircleShape),
                color = Color(0xFF6366F1),
                trackColor = Color.DarkGray
            )
        }

        // Live Coin Collector
        Row(
            modifier = Modifier
                .align(Alignment.TopStart)
                .padding(14.dp)
                .background(Color.Black.copy(0.7f), RoundedCornerShape(8.dp))
                .padding(horizontal = 10.dp, vertical = 6.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(Icons.Default.Star, contentDescription = "Coins", tint = Color(0xFFFFD700), modifier = Modifier.size(16.dp))
            Spacer(modifier = Modifier.width(4.dp))
            Text("${engine.playerCoinsCollected} COINS", color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
        }

        // Pause Menu selector
        IconButton(
            onClick = { viewModel.pauseGame() },
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(14.dp)
                .background(Color.Black.copy(alpha = 0.5f), CircleShape)
        ) {
            Icon(Icons.Default.Menu, contentDescription = "Pause", tint = Color.White)
        }

        // 3-2-1 RACER countdown Active
        if (engine.countdownActive) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Black.copy(0.4f)),
                contentAlignment = Alignment.Center
            ) {
                val integerSec = kotlin.math.ceil(engine.countdown).toInt()
                val displayStr = if (integerSec > 0) "$integerSec" else "GO!"
                
                LaunchedEffect(integerSec) {
                    if (integerSec > 0) {
                        viewModel.playBeepLow()
                    } else {
                        viewModel.playBeepHigh()
                    }
                }

                Text(
                    text = displayStr,
                    color = if (integerSec > 0) Color(0xFFFF3E3E) else Color(0xFF10B981),
                    fontSize = 80.sp,
                    fontWeight = FontWeight.Black,
                    fontFamily = FontFamily.Monospace
                )
            }
        }

        // =========================================================================
        // TOUCH CONTROLS PANEL OVERLAYS
        // =========================================================================
        if (!engine.countdownActive) {
            Box(modifier = Modifier.fillMaxSize()) {
                // Left Panel: Turning steering buttons
                Row(
                    modifier = Modifier
                        .align(Alignment.BottomStart)
                        .padding(24.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    Card(
                        modifier = Modifier
                            .size(72.dp)
                            .pointerInput(Unit) {
                                detectTapGestures(
                                    onPress = {
                                        try {
                                            engine.inputSteer = -1f
                                            awaitRelease()
                                        } finally {
                                            engine.inputSteer = 0f
                                        }
                                    }
                                )
                            },
                        shape = CircleShape,
                        colors = CardDefaults.cardColors(containerColor = Color.Black.copy(0.6f)),
                        border = BorderStroke(2.dp, Color(0xFF6366F1))
                    ) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Icon(Icons.Default.ArrowBack, contentDescription = "Left", tint = Color.White, modifier = Modifier.size(36.dp))
                        }
                    }

                    Card(
                        modifier = Modifier
                            .size(72.dp)
                            .pointerInput(Unit) {
                                detectTapGestures(
                                    onPress = {
                                        try {
                                            engine.inputSteer = 1f
                                            awaitRelease()
                                        } finally {
                                            engine.inputSteer = 0f
                                        }
                                    }
                                )
                            },
                        shape = CircleShape,
                        colors = CardDefaults.cardColors(containerColor = Color.Black.copy(0.6f)),
                        border = BorderStroke(2.dp, Color(0xFF6366F1))
                    ) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Icon(Icons.Default.ArrowForward, contentDescription = "Right", tint = Color.White, modifier = Modifier.size(36.dp))
                        }
                    }
                }

                // Right Panel: Pedals
                Row(
                    modifier = Modifier
                        .align(Alignment.BottomEnd)
                        .padding(24.dp),
                    verticalAlignment = Alignment.Bottom,
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    // Custom Nitro round trigger (shows electric blue lightning symbol text)
                    Box(modifier = Modifier.wrapContentSize()) {
                        val nBtnColor = if (engine.playerNitroLevel > 5f) Color(0xFF00E1FF) else Color.DarkGray
                        Card(
                            modifier = Modifier
                                .size(64.dp)
                                .pointerInput(Unit) {
                                    detectTapGestures(
                                        onPress = {
                                            try {
                                                engine.inputNitroActive = true
                                                awaitRelease()
                                            } finally {
                                                engine.inputNitroActive = false
                                            }
                                        }
                                    )
                                },
                            shape = CircleShape,
                            colors = CardDefaults.cardColors(containerColor = Color.Black.copy(0.6f)),
                            border = BorderStroke(1.5.dp, nBtnColor)
                        ) {
                            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                                Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                                    Text("⚡", color = nBtnColor, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                                    Text("NITRO", color = nBtnColor, fontSize = 8.sp, fontWeight = FontWeight.Bold)
                                }
                            }
                        }
                        
                        val levelPct = engine.playerNitroLevel / engine.maxNitroLevel
                        Spacer(
                            modifier = Modifier
                                .align(Alignment.BottomCenter)
                                .padding(bottom = 6.dp)
                                .width(36.dp)
                                .height(3.dp)
                                .background(Color(0xFF00D2D2).copy(alpha = levelPct.coerceIn(0f, 1f)))
                        )
                    }

                    // Brake Reverse Pedal
                    Card(
                        modifier = Modifier
                            .width(60.dp)
                            .height(84.dp)
                            .pointerInput(Unit) {
                                detectTapGestures(
                                    onPress = {
                                        try {
                                            engine.inputBrake = true
                                            awaitRelease()
                                        } finally {
                                            engine.inputBrake = false
                                        }
                                    }
                                )
                            },
                        shape = RoundedCornerShape(8.dp),
                        colors = CardDefaults.cardColors(containerColor = Color.Black.copy(0.6f)),
                        border = BorderStroke(1.5.dp, Color(0xFFEF4444))
                    ) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Text("▼", color = Color(0xFFEF4444), fontSize = 18.sp, fontWeight = FontWeight.Bold)
                                Spacer(modifier = Modifier.height(4.dp))
                                Text("REMAIN", color = Color.White, fontSize = 8.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
                            }
                        }
                    }

                    // Accelerate gas pedal
                    Card(
                        modifier = Modifier
                            .width(68.dp)
                            .height(105.dp)
                            .pointerInput(Unit) {
                                detectTapGestures(
                                    onPress = {
                                        try {
                                            engine.inputAccelerate = true
                                            awaitRelease()
                                        } finally {
                                            engine.inputAccelerate = false
                                        }
                                    }
                                )
                            },
                        shape = RoundedCornerShape(8.dp),
                        colors = CardDefaults.cardColors(containerColor = Color.Black.copy(0.6f)),
                        border = BorderStroke(2.dp, Color(0xFF10B981))
                    ) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Icon(Icons.Default.PlayArrow, contentDescription = "Gas", tint = Color(0xFF10B981), modifier = Modifier.size(28.dp))
                                Spacer(modifier = Modifier.height(4.dp))
                                Text("PEDAL", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
                            }
                        }
                    }
                }
            }
        }

        // 10. DIALOG PAUSE MENU
        if (isPaused) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Black.copy(0.75f)),
                contentAlignment = Alignment.Center
            ) {
                Card(
                    modifier = Modifier
                        .fillMaxWidth(0.42f)
                        .padding(16.dp),
                    colors = CardDefaults.cardColors(containerColor = Color(0xFF0F172A)),
                    border = BorderStroke(1.5.dp, Color(0xFF3B82F6).copy(0.6f))
                ) {
                    Column(
                        modifier = Modifier.padding(20.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        Text(
                            text = "GAMEPLAY DI-JEDA",
                            color = Color.White,
                            fontSize = 18.sp,
                            fontWeight = FontWeight.Bold,
                            fontFamily = FontFamily.Monospace
                        )
                        Spacer(modifier = Modifier.height(4.dp))

                        Button(
                            onClick = { viewModel.resumeGame() },
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF10B981)),
                            shape = RoundedCornerShape(6.dp),
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text("LANJUTKAN BALAPAN", fontWeight = FontWeight.Bold)
                        }

                        Button(
                            onClick = {
                                viewModel.startNewRace()
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF6366F1)),
                            shape = RoundedCornerShape(6.dp),
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text("ULANGI DARI AWAL", fontWeight = FontWeight.Bold)
                        }

                        Button(
                            onClick = { viewModel.cancelActiveRace() },
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFEF4444)),
                            shape = RoundedCornerShape(6.dp),
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text("KELUAR KE MENU UTAMA", fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }
    }
}

// =========================================================================
// 6. RACE RESULTS SCREEN
// =========================================================================
@Composable
fun ResultScreen(viewModel: GameViewModel) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF020617)),
        contentAlignment = Alignment.Center
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth(0.65f)
                .background(Color(0xFF0F172A), RoundedCornerShape(14.dp))
                .border(2.dp, Color(0xFFFFD700).copy(0.4f), RoundedCornerShape(14.dp))
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            val position = viewModel.finishPosition
            val isSuccess = viewModel.isCareerTargetPassed

            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = if (isSuccess) Icons.Default.Star else Icons.Default.Close,
                    contentDescription = "Reward Icon",
                    tint = if (isSuccess) Color(0xFFFFD700) else Color.Red,
                    modifier = Modifier.size(32.dp)
                )
                Spacer(modifier = Modifier.width(10.dp))
                val mainTitle = if (viewModel.currentGameMode == GameMode.CAREER) {
                    if (isSuccess) "STAGES CLEAN COMPLETED!" else "STAGE TARGET GAGAL!"
                } else {
                    "BALAPAN SELESAI FINISHED!"
                }
                Text(
                    text = mainTitle,
                    color = if (isSuccess) Color.White else Color(0xFFFF5252),
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Black,
                    fontFamily = FontFamily.Monospace
                )
            }

            HorizontalDivider(color = Color.White.copy(0.08f))

            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("POSISI FINISH AKHIR", color = Color.Gray, fontSize = 12.sp, fontFamily = FontFamily.Monospace)
                val placementSuffix = when(position) {
                    1 -> "1st Place (CHAMPION)"
                    2 -> "2nd Place"
                    3 -> "3rd Place"
                    else -> "${position}th Place"
                }
                Text(placementSuffix, color = if (position <= 3) Color.Yellow else Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
            }

            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("REKOR WAKTU LAP LINTASAN", color = Color.Gray, fontSize = 12.sp, fontFamily = FontFamily.Monospace)
                Text(viewModel.formattedRaceTime, color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
            }

            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("KOIN YANG DEBEROLEH", color = Color.Gray, fontSize = 12.sp, fontFamily = FontFamily.Monospace)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Star, contentDescription = "Gold Coins", tint = Color(0xFFFFD700), modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(4.dp))
                    Text("+ ${viewModel.coinsEarnedInRace} COINS", color = Color(0xFF10B981), fontSize = 13.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
                }
            }

            if (viewModel.currentGameMode == GameMode.CAREER) {
                val lvlName = when(viewModel.careerLevel.value - 1) {
                    1 -> "Sahara Dunes Stage unlocked!"
                    2 -> "Full Career Champion Trophy!"
                    else -> "Next stage ready to join!"
                }
                Spacer(modifier = Modifier.height(4.dp))
                if (isSuccess) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(Color(0xFF10B981).copy(0.15f), RoundedCornerShape(6.dp))
                            .padding(8.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "TARGET DIGAPAI! $lvlName",
                            color = Color(0xFF10B981),
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            fontFamily = FontFamily.Monospace
                        )
                    }
                } else {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(Color.Red.copy(0.1f), RoundedCornerShape(6.dp))
                            .padding(8.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        val requiredTarget = when (viewModel.careerLevel.value) {
                            1 -> "Sunset City: Minimum posisi 3"
                            2 -> "Emerald Forest: Minimum posisi 2"
                            else -> "Sahara Dunes: Wajib posisi 1"
                        }
                        Text(
                            text = "Target Gagal. Target: $requiredTarget",
                            color = Color(0xFFEF4444),
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold,
                            fontFamily = FontFamily.Monospace
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Button(
                    onClick = {
                        viewModel.playBeepHigh()
                        viewModel.startNewRace()
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF3B82F6)),
                    shape = RoundedCornerShape(6.dp),
                    modifier = Modifier.weight(1f)
                ) {
                    Text("COBA LAGI / REPLAY", fontWeight = FontWeight.Bold)
                }

                Button(
                    onClick = {
                        viewModel.playBeepLow()
                        viewModel.currentScreen = ScreenState.MAIN_MENU
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = Color.DarkGray),
                    shape = RoundedCornerShape(6.dp),
                    modifier = Modifier.weight(1f)
                ) {
                    Text("MENU UTAMA", color = Color.White)
                }
            }
        }
    }
}
