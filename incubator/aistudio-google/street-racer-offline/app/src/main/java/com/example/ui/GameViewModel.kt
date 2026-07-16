package com.example.ui

import android.app.Application
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.*
import com.example.game.*
import com.example.ui.components.SynthSoundManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

enum class ScreenState {
    MAIN_MENU,
    CAREER_OVERVIEW,
    CAR_SELECTION,
    TRACK_SELECTION,
    PLAYING,
    RESULT
}

enum class GameMode {
    CAREER,
    TIME_TRIAL,
    QUICK_RACE
}

class GameViewModel(application: Application) : AndroidViewModel(application) {
    private val database = GameDatabase.getDatabase(application)
    private val repository = GameRepository(database.gameDao())

    val soundManager = SynthSoundManager()

    // Specs Definitions
    val CAR_LIST = listOf(
        CarSpec("car_rookie", "Rookie Roadster", 190f, 1.0f, 1.0f, 1.0f, "#FFF13A3A", 0),
        CarSpec("car_forest", "Forest Fury", 210f, 1.2f, 1.4f, 1.1f, "#FF16A085", 150),
        CarSpec("car_desert", "Desert Storm", 230f, 1.35f, 1.05f, 1.3f, "#FFF39C12", 300),
        CarSpec("car_phantom", "Nitro Phantom", 250f, 1.3f, 1.25f, 1.8f, "#FF8E44AD", 500),
        CarSpec("car_hypersonic", "Hyper Sonic", 280f, 1.75f, 1.5f, 1.6f, "#FF2980B9", 800)
    )

    val TRACK_LIST = listOf(
        TrackSpec("track_city", "Sunset City", 2800f, 3, "#FF1B263B", "#FF1B4B27", "#FF212529", "Balapan metropolitan malam hari bermandikan lampu neon aspal datar.", 0.1f),
        TrackSpec("track_forest", "Emerald Forest", 3400f, 3, "#FF1F2F16", "#FF1A330E", "#FF3D2314", "Meluncur mulus di rimbun pepohonan pinus berliku tinggi.", 0.4f),
        TrackSpec("track_desert", "Sahara Dunes", 3900f, 3, "#FF5E300B", "#FFC68B59", "#FF4A3B32", "Balapan liar di padang pasir berbukit dengan badai debu deras.", 0.7f)
    )

    // Reactive State Flows
    private val _coins = MutableStateFlow(0)
    val coins: StateFlow<Int> = _coins.asStateFlow()

    private val _ownedCars = MutableStateFlow<Set<String>>(setOf("car_rookie"))
    val ownedCars: StateFlow<Set<String>> = _ownedCars.asStateFlow()

    private val _unlockedTracks = MutableStateFlow<Set<String>>(setOf("track_city"))
    val unlockedTracks: StateFlow<Set<String>> = _unlockedTracks.asStateFlow()

    private val _trackRecords = MutableStateFlow<Map<String, TrackRecord>>(emptyMap())
    val trackRecords: StateFlow<Map<String, TrackRecord>> = _trackRecords.asStateFlow()

    private val _careerLevel = MutableStateFlow(1)
    val careerLevel: StateFlow<Int> = _careerLevel.asStateFlow()

    // Game Layout Screen State Handles
    var currentScreen by mutableStateOf(ScreenState.MAIN_MENU)
    var selectedCarId by mutableStateOf("car_rookie")
    var selectedTrackId by mutableStateOf("track_city")
    var currentGameMode by mutableStateOf(GameMode.QUICK_RACE)

    // Engine Instances
    var activeEngine: RacingEngine? by mutableStateOf(null)
    var isPaused by mutableStateOf(false)
    var isMuted by mutableStateOf(false)
    var showStartBoosterCountdown by mutableStateOf(true)

    // Result States
    var finishPosition by mutableStateOf(6)
    var coinsEarnedInRace by mutableStateOf(0)
    var isCareerTargetPassed by mutableStateOf(false)
    var formattedRaceTime by mutableStateOf("0:00")

    init {
        loadProgressData()
    }

    private fun loadProgressData() {
        viewModelScope.launch {
            repository.userProgress.collectLatest { progress ->
                if (progress != null) {
                    _coins.value = progress.coins
                    selectedCarId = progress.selectedCarId
                    _careerLevel.value = progress.currentCareerLevel
                } else {
                    // Seed initial DB entry
                    repository.saveProgress(UserProgress(0, 0, "car_rookie", 1))
                }
            }
        }

        viewModelScope.launch {
            repository.ownedCars.collectLatest { list ->
                if (list.isNotEmpty()) {
                    _ownedCars.value = list.map { it.carId }.toSet()
                } else {
                    repository.unlockCar("car_rookie")
                }
            }
        }

        viewModelScope.launch {
            repository.unlockedTracks.collectLatest { list ->
                if (list.isNotEmpty()) {
                    _unlockedTracks.value = list.map { it.trackId }.toSet()
                } else {
                    repository.unlockTrack("track_city")
                }
            }
        }

        viewModelScope.launch {
            repository.trackRecords.collectLatest { list ->
                _trackRecords.value = list.associateBy { it.trackId }
            }
        }
    }

    fun playBeepLow() = soundManager.playBeepLow()
    fun playBeepHigh() = soundManager.playBeepHigh()

    fun toggleMute() {
        isMuted = !isMuted
        soundManager.setMute(isMuted)
    }

    fun buyCar(carSpec: CarSpec) {
        if (coins.value >= carSpec.price && !ownedCars.value.contains(carSpec.id)) {
            viewModelScope.launch {
                val newCoins = coins.value - carSpec.price
                _coins.value = newCoins
                repository.saveProgress(UserProgress(0, newCoins, carSpec.id, careerLevel.value))
                repository.unlockCar(carSpec.id)
                selectedCarId = carSpec.id
                soundManager.playCoinSound()
            }
        }
    }

    fun selectCar(carId: String) {
        if (ownedCars.value.contains(carId)) {
            selectedCarId = carId
            viewModelScope.launch {
                repository.saveProgress(UserProgress(0, coins.value, carId, careerLevel.value))
            }
        }
    }

    fun buyTrack(trackSpec: TrackSpec, price: Int) {
        if (coins.value >= price && !unlockedTracks.value.contains(trackSpec.id)) {
            viewModelScope.launch {
                val newCoins = coins.value - price
                _coins.value = newCoins
                repository.saveProgress(UserProgress(0, newCoins, selectedCarId, careerLevel.value))
                repository.unlockTrack(trackSpec.id)
                selectedTrackId = trackSpec.id
                soundManager.playCoinSound()
            }
        }
    }

    fun startNewRace() {
        val car = CAR_LIST.find { it.id == selectedCarId } ?: CAR_LIST[0]
        val track = TRACK_LIST.find { it.id == selectedTrackId } ?: TRACK_LIST[0]

        val engine = RacingEngine(track, car)
        // If Time Trial, remove AIs (leave only player)
        if (currentGameMode == GameMode.TIME_TRIAL) {
            val playerOnly = engine.racers.filter { it.isPlayer }
            engine.racers.clear()
            engine.racers.addAll(playerOnly)
        }

        activeEngine = engine
        isPaused = false
        currentScreen = ScreenState.PLAYING
        soundManager.updateEnginePitch(0f)
        soundManager.setMute(isMuted)
    }

    fun resumeGame() {
        isPaused = false
    }

    fun pauseGame() {
        isPaused = true
    }

    fun cancelActiveRace() {
        activeEngine = null
        isPaused = false
        currentScreen = ScreenState.MAIN_MENU
    }

    fun completeRaceSimulation(engine: RacingEngine) {
        val player = engine.racers.find { it.isPlayer } ?: return
        finishPosition = player.currentPosition

        // Format Race Time
        val totalMs = player.finishTimeMillis
        val minutes = (totalMs / 60000).toInt()
        val seconds = ((totalMs % 60000) / 1000).toInt()
        val tenths = ((totalMs % 1000) / 100).toInt()
        formattedRaceTime = String.format("%02d:%02d.%01d", minutes, seconds, tenths)

        // Calculate Coins logic
        var coinBonus = engine.playerCoinsCollected

        if (currentGameMode == GameMode.TIME_TRIAL) {
            // Earn coins based on keeping time minimum
            val targetTimeTrial = engine.trackSpec.length * 0.90f * 60f // estimated target units time
            val actualTimeUnits = totalMs / 1000f
            if (actualTimeUnits < targetTimeTrial) {
                coinBonus += 40
            } else {
                coinBonus += 15
            }
            isCareerTargetPassed = true
        } else if (currentGameMode == GameMode.CAREER) {
            // Evaluasi target karir
            evaluateCareerSuccess(engine, player, coinBonus)
        } else {
            // QUICK RACE
            val placementReward = when (finishPosition) {
                1 -> 50
                2 -> 35
                3 -> 20
                else -> 8
            }
            coinBonus += placementReward
            isCareerTargetPassed = true
        }

        coinsEarnedInRace = coinBonus

        // Save Results and update user progress database record
        viewModelScope.launch {
            val newCoins = coins.value + coinsEarnedInRace
            _coins.value = newCoins

            // Save Record
            val existingRecord = trackRecords.value[selectedTrackId]
            val bestMs = if (existingRecord == null) totalMs else Math.min(existingRecord.bestTimeMillis, totalMs)
            val bestPos = if (existingRecord == null) finishPosition else Math.min(existingRecord.highPosition, finishPosition)
            repository.saveRecord(TrackRecord(selectedTrackId, bestMs, bestPos))

            repository.saveProgress(UserProgress(0, newCoins, selectedCarId, careerLevel.value))
        }

        soundManager.playVictorySound()
        currentScreen = ScreenState.RESULT
    }

    private fun evaluateCareerSuccess(engine: RacingEngine, player: RacerState, baseBonus: Int) {
        var rewards = 0
        var careerPassed = false
        val currentLvl = careerLevel.value

        when (currentLvl) {
            1 -> {
                // Sunset City, must be 3rd or better
                if (finishPosition <= 3) {
                    rewards = 100
                    careerPassed = true
                    viewModelScope.launch {
                        repository.saveProgress(UserProgress(0, coins.value, selectedCarId, 2))
                        _careerLevel.value = 2
                        // Auto unlock track forest
                        repository.unlockTrack("track_forest")
                    }
                }
            }
            2 -> {
                // Forest, must be 2nd or better
                if (finishPosition <= 2) {
                    rewards = 200
                    careerPassed = true
                    viewModelScope.launch {
                        repository.saveProgress(UserProgress(0, coins.value, selectedCarId, 3))
                        _careerLevel.value = 3
                        // Auto unlock track desert
                        repository.unlockTrack("track_desert")
                    }
                }
            }
            3 -> {
                // Desert, must be 1st
                if (finishPosition == 1) {
                    rewards = 350
                    careerPassed = true
                    viewModelScope.launch {
                        repository.saveProgress(UserProgress(0, coins.value, selectedCarId, 4))
                        _careerLevel.value = 4
                    }
                }
            }
            else -> {
                // Free race at infinite tier levels
                if (finishPosition == 1) {
                    rewards = 150
                    careerPassed = true
                }
            }
        }

        coinsEarnedInRace = baseBonus + rewards
        isCareerTargetPassed = careerPassed
    }

    fun resetSaveData() {
        viewModelScope.launch {
            // Delete and regenerate tables using default initialization
            withContext(Dispatchers.IO) {
                database.clearAllTables()
            }
            // Seed initial records
            repository.saveProgress(UserProgress(0, 0, "car_rookie", 1))
            repository.unlockCar("car_rookie")
            repository.unlockTrack("track_city")
            
            _coins.value = 0
            _careerLevel.value = 1
            selectedCarId = "car_rookie"
            selectedTrackId = "track_city"
            currentGameMode = GameMode.QUICK_RACE
            currentScreen = ScreenState.MAIN_MENU
        }
    }

    override fun onCleared() {
        super.onCleared()
        soundManager.release()
    }
}
