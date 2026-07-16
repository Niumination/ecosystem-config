package com.example.data

import android.content.Context
import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Entity(tableName = "user_progress")
data class UserProgress(
    @PrimaryKey val id: Int = 0,
    val coins: Int = 0,
    val selectedCarId: String = "car_rookie",
    val currentCareerLevel: Int = 1
)

@Entity(tableName = "owned_cars")
data class OwnedCar(
    @PrimaryKey val carId: String
)

@Entity(tableName = "unlocked_tracks")
data class UnlockedTrack(
    @PrimaryKey val trackId: String
)

@Entity(tableName = "track_records")
data class TrackRecord(
    @PrimaryKey val trackId: String,
    val bestTimeMillis: Long = Long.MAX_VALUE,
    val highPosition: Int = 99
)

@Dao
interface GameDao {
    @Query("SELECT * FROM user_progress WHERE id = 0")
    fun getUserProgress(): Flow<UserProgress?>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun saveUserProgress(progress: UserProgress)

    @Query("SELECT * FROM owned_cars")
    fun getOwnedCars(): Flow<List<OwnedCar>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun addOwnedCar(car: OwnedCar)

    @Query("SELECT * FROM unlocked_tracks")
    fun getUnlockedTracks(): Flow<List<UnlockedTrack>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun addUnlockedTrack(track: UnlockedTrack)

    @Query("SELECT * FROM track_records")
    fun getTrackRecords(): Flow<List<TrackRecord>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun saveTrackRecord(record: TrackRecord)
}

@Database(entities = [UserProgress::class, OwnedCar::class, UnlockedTrack::class, TrackRecord::class], version = 1, exportSchema = false)
abstract class GameDatabase : RoomDatabase() {
    abstract fun gameDao(): GameDao

    companion object {
        @Volatile
        private var INSTANCE: GameDatabase? = null

        fun getDatabase(context: Context): GameDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    GameDatabase::class.java,
                    "street_racer_db"
                )
                .fallbackToDestructiveMigration()
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}

class GameRepository(private val gameDao: GameDao) {
    val userProgress: Flow<UserProgress?> = gameDao.getUserProgress()
    val ownedCars: Flow<List<OwnedCar>> = gameDao.getOwnedCars()
    val unlockedTracks: Flow<List<UnlockedTrack>> = gameDao.getUnlockedTracks()
    val trackRecords: Flow<List<TrackRecord>> = gameDao.getTrackRecords()

    suspend fun saveProgress(progress: UserProgress) {
        gameDao.saveUserProgress(progress)
    }

    suspend fun unlockCar(carId: String) {
        gameDao.addOwnedCar(OwnedCar(carId))
    }

    suspend fun unlockTrack(trackId: String) {
        gameDao.addUnlockedTrack(UnlockedTrack(trackId))
    }

    suspend fun saveRecord(record: TrackRecord) {
        gameDao.saveTrackRecord(record)
    }
}
