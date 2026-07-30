# Jetpack Compose — UI Polish Patterns

Custom theme → animated NavHost → splash screen → staggered entrance → animated indicators.

## 1. Custom Material3 Color Scheme

**File:** `ui/theme/Color.kt`

Define brand colors upfront:

```kotlin
val Emerald400 = Color(0xFF34D399)
val Emerald600 = Color(0xFF059669)
val Teal400 = Color(0xFF2DD4BF)
val SurfaceDark = Color(0xFF0F172A)
val SurfaceLight = Color(0xFFF8FAFC)
```

**File:** `ui/theme/Theme.kt`

Create full dark + light schemes referencing brand colors:

```kotlin
private val DarkColorScheme = darkColorScheme(
    primary = Emerald400,
    onPrimary = Emerald900,
    primaryContainer = Emerald800,
    onPrimaryContainer = Emerald200,
    secondary = Teal400,
    surface = Color(0xFF1E293B),
    onSurface = Color(0xFFE2E8F0),
    surfaceVariant = Color(0xFF334155),
    // ... keep going for all Material3 keys
)
```

Respect dynamic color (Android 12+) but fall back to custom scheme:

```kotlin
val colorScheme = when {
    dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
        val ctx = LocalContext.current
        if (darkTheme) dynamicDarkColorScheme(ctx) else dynamicLightColorScheme(ctx)
    }
    darkTheme -> DarkColorScheme
    else -> LightColorScheme
}
MaterialTheme(colorScheme = colorScheme, typography = Typography, content = content)
```

> **Tip:** Override ALL color keys (`primary`, `onPrimary`, `primaryContainer`, `onPrimaryContainer`, `secondary`, `secondaryContainer`, `tertiary`, `background`, `surface`, `surfaceVariant`, `onSurface`, `onSurfaceVariant`, `outline`, `outlineVariant`, `error`, etc.) for a consistent look across all Material3 components.

## 2. Full Typography Scale

**File:** `ui/theme/Type.kt`

Define all 13 Material3 text styles for consistency:

```kotlin
val Typography = Typography(
    displayLarge = TextStyle(fontWeight = Bold, fontSize = 36.sp, lineHeight = 44.sp),
    displayMedium = TextStyle(fontWeight = Bold, fontSize = 28.sp, lineHeight = 36.sp),
    headlineLarge = TextStyle(fontWeight = Bold, fontSize = 24.sp, lineHeight = 32.sp),
    headlineMedium = TextStyle(fontWeight = SemiBold, fontSize = 20.sp, lineHeight = 28.sp),
    titleLarge = TextStyle(fontWeight = Bold, fontSize = 22.sp, lineHeight = 28.sp),
    titleMedium = TextStyle(fontWeight = SemiBold, fontSize = 16.sp, lineHeight = 24.sp),
    titleSmall = TextStyle(fontWeight = Medium, fontSize = 14.sp, lineHeight = 20.sp),
    bodyLarge = TextStyle(fontSize = 16.sp, lineHeight = 24.sp),
    bodyMedium = TextStyle(fontSize = 14.sp, lineHeight = 20.sp),
    bodySmall = TextStyle(fontSize = 12.sp, lineHeight = 16.sp, letterSpacing = 0.4.sp),
    labelLarge = TextStyle(fontWeight = Medium, fontSize = 14.sp),
    labelMedium = TextStyle(fontWeight = Medium, fontSize = 12.sp),
    labelSmall = TextStyle(fontWeight = Medium, fontSize = 11.sp),
)
```

## 3. Animated NavHost (Screen Transitions)

**File:** `MainActivity.kt`

Replace default `NavHost` with animated transitions:

```kotlin
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally

private const val ANIM_DURATION = 300

NavHost(
    navController = nav,
    startDestination = "home",
    enterTransition = {
        slideInHorizontally(initialOffsetX = { it }, animationSpec = tween(ANIM_DURATION)) +
        fadeIn(animationSpec = tween(ANIM_DURATION))
    },
    exitTransition = {
        slideOutHorizontally(targetOffsetX = { -it / 3 }, animationSpec = tween(ANIM_DURATION)) +
        fadeOut(animationSpec = tween(ANIM_DURATION))
    },
    popEnterTransition = {
        slideInHorizontally(initialOffsetX = { -it / 3 }, animationSpec = tween(ANIM_DURATION)) +
        fadeIn(animationSpec = tween(ANIM_DURATION))
    },
    popExitTransition = {
        slideOutHorizontally(targetOffsetX = { it }, animationSpec = tween(ANIM_DURATION)) +
        fadeOut(animationSpec = tween(ANIM_DURATION))
    },
)
```

**Transition logic:**
- **Forward (enter):** slide in from right → user feels "going deeper"
- **Back/Exit:** slide out to left + small slide → the old page shrinks away
- **Pop back (enter):** previous page slides back from left edge
- **Pop back (exit):** current page slides out to the right

## 4. Splash Screen (core-splashscreen)

### Dependency (`app/build.gradle.kts`)

```kotlin
implementation("androidx.core:core-splashscreen:1.0.1")
```

### XML Theme (`res/values/themes.xml`)

```xml
<style name="Theme.AppName.Splash" parent="Theme.SplashScreen">
    <item name="windowSplashScreenBackground">#059669</item>
    <item name="windowSplashScreenAnimatedIcon">@mipmap/ic_launcher</item>
    <item name="postSplashScreenTheme">@style/Theme.AppName</item>
</style>
```

### Activity Theme (`AndroidManifest.xml`)

```xml
<activity
    android:name=".MainActivity"
    android:theme="@style/Theme.AppName.Splash">
```

### Activity Code (`MainActivity.kt`)

```kotlin
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import androidx.activity.enableEdgeToEdge

override fun onCreate(savedInstanceState: Bundle?) {
    installSplashScreen()
    enableEdgeToEdge()
    super.onCreate(savedInstanceState)
    // ... setContent { ... }
}
```

## 5. Staggered Entrance Animation (per screen)

**Pattern:** control visibility state with `LaunchedEffect` + staggered delay, wrap sections in `AnimatedVisibility`.

```kotlin
var visible by remember { mutableStateOf(false) }
LaunchedEffect(Unit) {
    delay(80)  // small initial delay after screen mount
    visible = true
}

// Then wrap each section with increasing delay
AnimatedVisibility(
    visible = visible,
    enter = fadeIn(tween(300)) + slideInVertically(tween(300)) { it / 2 },
) { Section1() }

AnimatedVisibility(
    visible = visible,
    enter = fadeIn(tween(500)) + slideInVertically(tween(500)) { it / 2 },
) { Section2() }

AnimatedVisibility(
    visible = visible,
    enter = fadeIn(tween(700)) + slideInVertically(tween(700)) { it / 2 },
) { Section3() }
```

For LazyColumn items, use `itemsIndexed` + `AnimatedVisibility` with staggered delay based on index:

```kotlin
itemsIndexed(items) { index, item ->
    AnimatedVisibility(
        visible = true,
        enter = fadeIn(tween(300 + index * 50)) + slideInVertically(tween(300 + index * 50)) { it / 3 },
    ) { ItemCard(item) }
}
```

## 6. Pulsing Scanning Indicator

```kotlin
@Composable
fun PulsingIndicator(msg: String) {
    val infiniteTransition = rememberInfiniteTransition(label = "pulse")
    val pulse by infiniteTransition.animateFloat(
        initialValue = 0.6f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(800),
            repeatMode = RepeatMode.Reverse,
        ),
        label = "pulse",
    )

    Box(contentAlignment = Alignment.Center, modifier = Modifier.size(80.dp)) {
        CircularProgressIndicator(
            modifier = Modifier.fillMaxSize(),
            color = MaterialTheme.colorScheme.primary,
            strokeWidth = 5.dp,
        )
        // Inner pulsing dot
        Box(
            modifier = Modifier
                .size(32.dp)
                .scale(pulse)
                .alpha(pulse)
                .background(MaterialTheme.colorScheme.primary, CircleShape),
        )
    }
    Text(msg, style = MaterialTheme.typography.titleMedium)
}
```

## 7. Complete File Checklist

When polishing a Compose app, touch these files:

| File | Role |
|------|------|
| `ui/theme/Color.kt` (🆕) | Brand color constants |
| `ui/theme/Theme.kt` | Full dark/light scheme |
| `ui/theme/Type.kt` | Complete typography scale |
| `MainActivity.kt` | Splash + animated NavHost |
| `res/values/themes.xml` | Splash screen XML theme |
| `AndroidManifest.xml` | Activity uses splash theme |
| `app/build.gradle.kts` | `core-splashscreen` dep |
| Each `*Screen.kt` | Staggered entrance `AnimatedVisibility` |
