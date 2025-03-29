import streamlit as st
import time
import random
from PIL import Image, ImageDraw
import numpy as np
import base64
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="Retro Pixel Platformer", page_icon="🎮", layout="centered"
)


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

.stApp {
    background: linear-gradient(to bottom, #121212, #000000);
    font-family: 'Press Start 2P', monospace;
    color: #fff;
}

.title {
    text-align: center;
    color: #FFD700;
    font-size: 36px;
    text-shadow: 2px 2px #ff5a5f;
    margin-bottom: 30px;
    letter-spacing: 1px;
}

.game-container {
    border: 5px double #FFD700;
    border-radius: 10px;
    background-color: #111;
    padding: 12px;
    margin: auto;
}

.stats div {
    font-size: 14px;
    padding: 6px 10px;
    border-radius: 5px;
    background-color: rgba(255,255,255,0.1);
    margin: 0 5px;
}

button[kind="primary"] {
    background-color: #ff5a5f !important;
    color: white !important;
    border: 2px solid #FFD700 !important;
    border-radius: 5px;
    font-family: 'Press Start 2P', monospace;
    font-size: 10px !important;
    box-shadow: 0 0 6px #FFD700;
}

button[kind="primary"]:hover {
    background-color: #ff8080 !important;
    color: black !important;
}

.footer {
    text-align: center;
    font-size: 12px;
    margin-top: 40px;
    color: #aaa;
    opacity: 0.8;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

html, body, [class*="css"] {
    font-family: 'Press Start 2P', monospace;
    background: linear-gradient(180deg, #111 0%, #000 100%);
    color: #f1f1f1;
}

/* Title Bar */
.title {
    text-align: center;
    font-size: 28px;
    color: #00ffe5;
    margin-bottom: 20px;
    padding: 20px;
    text-shadow: 0 0 5px #00ffe5, 0 0 10px #007575;
    border-top: 4px solid #00ffe5;
    border-bottom: 4px solid #00ffe5;
    background: repeating-linear-gradient(
        45deg,
        #001f1d,
        #001f1d 10px,
        #000 10px,
        #000 20px
    );
    box-shadow: 0 0 20px #00ffe588;
}

/* Stats Row */
.stats {
    display: flex;
    justify-content: space-evenly;
    margin: 20px 0;
}

.stats div {
    font-size: 12px;
    background: #111;
    padding: 8px 14px;
    border: 2px solid #00ffe5;
    border-radius: 8px;
    color: #fff;
    box-shadow: inset 0 0 5px #00ffe5, 0 0 8px #00ffe599;
}

/* Buttons */
button[kind="primary"] {
    background: #00ffe5 !important;
    color: black !important;
    border: 2px solid #00ffe5 !important;
    border-radius: 6px;
    padding: 12px 20px;
    font-size: 10px !important;
    box-shadow: 0 0 10px #00ffe5;
    font-family: 'Press Start 2P', monospace;
}

button[kind="primary"]:hover {
    background: #00bba5 !important;
    color: white !important;
    border-color: #00bba5 !important;
}

/* Instructions */
.instructions {
    background: #1c1c1c;
    border: 2px dashed #00ffe5;
    padding: 16px;
    font-size: 11px;
    color: #f0f0f0;
    border-radius: 10px;
    text-align: center;
    margin-top: 20px;
    box-shadow: 0 0 10px #00ffe555;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 10px;
    color: #999;
    margin-top: 40px;
    text-shadow: 0 0 5px #00ffe5;
    opacity: 0.8;
}
/* Make default button look retro-cool */
.stButton > button {
    background: #00ffe5 !important;
    color: black !important;
    border: 4px solid #00ffe5 !important;
    border-radius: 10px !important;
    font-family: 'Press Start 2P', monospace !important;
    font-size: 14px !important;
    padding: 16px 32px !important;
    text-align: center !important;
    box-shadow: 0 0 20px #00ffe5, inset 0 0 10px #00ffe5 !important;
    transition: all 0.2s ease-in-out !important;
    width: auto !important;
    margin: 30px auto !important;
    display: block !important;
}

.stButton > button:hover {
    background: #00bfa5 !important;
    color: white !important;
    box-shadow: 0 0 30px #00ffe5, inset 0 0 15px #00ffe5 !important;
}
            
/* Hide Streamlit's default header */
header[data-testid="stHeader"] {
    visibility: hidden;
}

/* Optional: remove top padding caused by hidden header */
main > div:first-child {
    padding-top: 0rem;
}

</style>
""",
    unsafe_allow_html=True,
)


# Game state
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "player_x" not in st.session_state:
    st.session_state.player_x = 50
if "player_y" not in st.session_state:
    st.session_state.player_y = 200
if "jump_count" not in st.session_state:
    st.session_state.jump_count = 0
if "is_jumping" not in st.session_state:
    st.session_state.is_jumping = False
if "score" not in st.session_state:
    st.session_state.score = 0
if "lives" not in st.session_state:
    st.session_state.lives = 3
if "collectibles" not in st.session_state:
    st.session_state.collectibles = []
if "platforms" not in st.session_state:
    st.session_state.platforms = []
if "level" not in st.session_state:
    st.session_state.level = 1
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Game constants
GAME_WIDTH = 800
GAME_HEIGHT = 400
PLAYER_SIZE = 20
GRAVITY = 4
JUMP_POWER = 15
MOVE_SPEED = 10
PLATFORM_HEIGHT = 10
COLLECTIBLE_SIZE = 15


# Create pixel art images
def create_pixel_image(width, height, draw_func):
    scale = 1
    img = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_func(draw, scale)
    return img


def get_image_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


# Create player sprite
def draw_player(draw, scale):
    # Body - blue color
    color = "#5b6ee1"
    # 5x5 pixel art character
    pixels = [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
    ]
    for y, row in enumerate(pixels):
        for x, pixel in enumerate(row):
            if pixel:
                draw.rectangle(
                    [
                        x * 4 * scale,
                        y * 4 * scale,
                        (x + 1) * 4 * scale,
                        (y + 1) * 4 * scale,
                    ],
                    fill=color,
                )


player_img = create_pixel_image(PLAYER_SIZE, PLAYER_SIZE, draw_player)
player_img_b64 = get_image_base64(player_img)


# Create collectible sprite (coin)
def draw_collectible(draw, scale, color="#ffd700"):

    # 4x4 pixel art coin
    pixels = [[0, 1, 1, 0], [1, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 0]]
    for y, row in enumerate(pixels):
        for x, pixel in enumerate(row):
            if pixel:
                draw.rectangle(
                    [
                        x * 4 * scale,
                        y * 4 * scale,
                        (x + 1) * 4 * scale,
                        (y + 1) * 4 * scale,
                    ],
                    fill=color,
                )


# collectible_img = create_pixel_image(COLLECTIBLE_SIZE, COLLECTIBLE_SIZE, draw_collectible)
# collectible_img_b64 = get_image_base64(collectible_img)


# Create platform sprite
def draw_platform(draw, scale, width):
    # Green color
    color = "#50c878"
    for x in range(width // 4):
        draw.rectangle(
            [x * 4 * scale, 0, (x + 1) * 4 * scale, PLATFORM_HEIGHT * scale], fill=color
        )


# Generate a level
def generate_level():
    st.session_state.platforms = []
    st.session_state.collectibles = []

    def is_overlapping(new_x, new_y, new_w):
        for p in st.session_state.platforms:
            existing_x = p["x"]
            existing_y = p["y"]
            existing_w = p["width"]
            if abs(new_y - existing_y) < 25 and not (  # vertical overlap threshold
                new_x + new_w < existing_x or new_x > existing_x + existing_w
            ):
                return True
        return False

    # Add ground platform
    st.session_state.platforms.append(
        {"x": 0, "y": GAME_HEIGHT - 20, "width": GAME_WIDTH}
    )

    # Add random platforms
    num_platforms = 5 + st.session_state.level
    attempts = 0

    for _ in range(num_platforms):
        width = random.randint(60, 150)
        x = random.randint(0, GAME_WIDTH - width)
        y = random.randint(80, GAME_HEIGHT - 50)
        if not is_overlapping(x, y, width):
            st.session_state.platforms.append({"x": x, "y": y, "width": width})
        attempts += 1
        # st.session_state.platforms.append({
        #     'x': random.randint(0, GAME_WIDTH - width),
        #     'y': random.randint(100, GAME_HEIGHT - 50),
        #     'width': width
        # })

    def is_collectible_overlapping(new_x, new_y):
        for p in st.session_state.platforms:
            # Check if collectible intersects with the platform
            if (
                new_x + COLLECTIBLE_SIZE > p["x"]
                and new_x < p["x"] + p["width"]
                and new_y + COLLECTIBLE_SIZE > p["y"]
                and new_y < p["y"] + PLATFORM_HEIGHT
            ):
                return True
        return False

    # Add collectibles
    num_collectibles = 5 + st.session_state.level * 2
    for _ in range(num_collectibles):
        placed = False
        attempts = 0
        # Place collectibles on platforms or in the air
        if random.random() > 0.3:  # 70% on platforms
            platform = random.choice(st.session_state.platforms)
            x = random.randint(
                platform["x"], platform["x"] + platform["width"] - COLLECTIBLE_SIZE
            )
            y = platform["y"] - COLLECTIBLE_SIZE - 5
        else:  # 30% in the air
            x = random.randint(0, GAME_WIDTH - COLLECTIBLE_SIZE)
            y = random.randint(50, GAME_HEIGHT - 100)

        # Check if the collectible overlaps with platforms
        if not is_collectible_overlapping(x, y):
            st.session_state.collectibles.append(
                {"x": x, "y": y, "collected": False, "type": "coin"}  # Default type
            )
            placed = True
        # attempts += 1
        # st.session_state.collectibles.append({
        #     'x': x,
        #     'y': y,
        #     'collected': False,
        #     'type': 'coin'  # Default type
        # })

    # Add a special gem collectible (worth more points)
    st.session_state.collectibles.append(
        {
            "x": random.randint(0, GAME_WIDTH - COLLECTIBLE_SIZE),
            "y": random.randint(50, 150),
            "collected": False,
            "type": "gem",
            "color": "#FFFFFF",  # Magenta for the special gem
        }
    )


# Game loop logic
def update_game():
    if not st.session_state.game_started or st.session_state.game_over:
        return

    # Apply gravity
    st.session_state.player_y += GRAVITY

    # Handle jumping
    if st.session_state.is_jumping:
        st.session_state.player_y -= JUMP_POWER - (st.session_state.jump_count // 2)
        st.session_state.jump_count += 1
        if st.session_state.jump_count > 10:
            st.session_state.is_jumping = False
            st.session_state.jump_count = 0

    # Check platform collisions
    on_platform = False
    for platform in st.session_state.platforms:

        if (
            st.session_state.player_x + PLAYER_SIZE > platform["x"]
            and st.session_state.player_x < platform["x"] + platform["width"]
        ):
            # # Check if player is landing on the platform
            if (
                st.session_state.player_y + PLAYER_SIZE >= platform["y"]
                and st.session_state.player_y + PLAYER_SIZE
                <= platform["y"] + PLATFORM_HEIGHT + 5
            ):
                st.session_state.player_y = platform["y"] - PLAYER_SIZE
                on_platform = True
                st.session_state.is_jumping = False
                st.session_state.jump_count = 0

            # Handle jumping up (bottom to top) - Allow the player to pass up through platform
            if (
                st.session_state.player_y + PLAYER_SIZE > platform["y"]
                and st.session_state.player_y < platform["y"] + PLATFORM_HEIGHT
            ):

                # Stop the player from going through the platform from the bottom (jumping up)
                st.session_state.player_y = platform["y"] + PLATFORM_HEIGHT

    # Check collectible collection
    for i, collectible in enumerate(st.session_state.collectibles):
        if not collectible["collected"]:
            if (
                st.session_state.player_x + PLAYER_SIZE > collectible["x"]
                and st.session_state.player_x < collectible["x"] + COLLECTIBLE_SIZE
                and st.session_state.player_y + PLAYER_SIZE > collectible["y"]
                and st.session_state.player_y < collectible["y"] + COLLECTIBLE_SIZE
            ):
                st.session_state.collectibles[i]["collected"] = True
                if collectible["type"] == "gem":
                    st.session_state.score += 5
                else:
                    st.session_state.score += 1

    # Check if all collectibles are collected (level complete)
    if all(c["collected"] for c in st.session_state.collectibles):
        st.session_state.level += 1
        generate_level()
        st.session_state.player_x = 50
        st.session_state.player_y = 200

    # Check if player falls off the screen
    fall_threshold = GAME_HEIGHT - 41
    if st.session_state.player_y > fall_threshold or st.session_state.player_y == -10:
        st.session_state.lives -= 1
        st.session_state.player_x = 50
        st.session_state.player_y = 200

        if st.session_state.lives <= 0:
            st.session_state.game_over = True

    # Keep player within game bounds
    st.session_state.player_x = max(
        0, min(st.session_state.player_x, GAME_WIDTH - PLAYER_SIZE)
    )
    st.session_state.player_y = max(0, st.session_state.player_y)


# Draw the game
def draw_game():
    # Create HTML5 canvas for better rendering
    html = f"""
    <div class="game-container" style="width: {GAME_WIDTH}px; height: {GAME_HEIGHT}px; position: relative; overflow: hidden;">
    """

    # Draw platforms
    for platform in st.session_state.platforms:
        platform_img = create_pixel_image(
            platform["width"],
            PLATFORM_HEIGHT,
            lambda draw, scale: draw_platform(draw, scale, platform["width"]),
        )
        platform_img_b64 = get_image_base64(platform_img)
        html += f"""
        <div style="position: absolute; left: {platform['x']}px; top: {platform['y']}px;">
            <img src="data:image/png;base64,{platform_img_b64}" style="width: {platform['width']}px; height: {PLATFORM_HEIGHT}px;">
        </div>
        """

    # Draw collectibles
    for collectible in st.session_state.collectibles:

        if not collectible["collected"]:

            # Different image for gem vs coin
            if collectible["type"] == "gem":
                color = "#00FFFF"  # Magenta for gem
            else:
                color = "#FFD700"  # Gold for coin

            collectible_img = create_pixel_image(
                COLLECTIBLE_SIZE,
                COLLECTIBLE_SIZE,
                lambda draw, scale: draw_collectible(draw, scale, color=color),
            )
            collectible_img_b64 = get_image_base64(collectible_img)

            html += f"""
            <div style="position: absolute; left: {collectible['x']}px; top: {collectible['y']}px;">
                <img src="data:image/png;base64,{collectible_img_b64}" style="width: {COLLECTIBLE_SIZE}px; height: {COLLECTIBLE_SIZE}px;">
            </div>
            """

    # Draw player
    html += f"""
    <div style="position: absolute; left: {st.session_state.player_x}px; top: {st.session_state.player_y}px;">
        <img src="data:image/png;base64,{player_img_b64}" style="width: {PLAYER_SIZE}px; height: {PLAYER_SIZE}px;">
    </div>
    """

    html += "</div>"
    return html


# Handle controls
def move_left():
    st.session_state.player_x -= MOVE_SPEED


def move_right():
    st.session_state.player_x += MOVE_SPEED


def jump():
    if not st.session_state.is_jumping:
        st.session_state.is_jumping = True
        st.session_state.jump_count = 0


def start_game():
    st.session_state.game_started = True
    st.session_state.player_x = 50
    st.session_state.player_y = 200
    st.session_state.score = 0
    st.session_state.lives = 3
    st.session_state.level = 1
    st.session_state.game_over = False
    generate_level()


def reset_game():
    start_game()


# Main app
st.markdown('<h1 class="title">🎮RETRO PIXEL PLATFORMER🎮</h1>', unsafe_allow_html=True)
st.markdown(
    f"""
<div class="stats">
    <div>🟡 SCORE: {st.session_state.score}</div>
    <div>🟥 LEVEL: {st.session_state.level}</div>
    <div>🟢 LIVES: {st.session_state.lives}</div>
</div>
""",
    unsafe_allow_html=True,
)
# COMMENTING FOR NOW
# # Game status display
# col1, col2, col3 = st.columns(3)
# # with col1:
# #     st.markdown(f"<div style='text-align: left; font-size: 24px; color: #ffd700;'>SCORE: {st.session_state.score}</div>", unsafe_allow_html=True)
# # with col2:
# #     st.markdown(f"<div style='text-align: center; font-size: 24px; color: #ff5a5f;'>LEVEL: {st.session_state.level}</div>", unsafe_allow_html=True)
# # with col3:
# #     st.markdown(f"<div style='text-align: right; font-size: 24px; color: #50c878;'>LIVES: {st.session_state.lives}</div>", unsafe_allow_html=True)

# Game canvas
if st.session_state.game_started and not st.session_state.game_over:
    update_game()
    game_html = draw_game()
    import streamlit.components.v1 as components

    components.html(game_html, height=GAME_HEIGHT, width=GAME_WIDTH)

    # Game controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Left", key="left", use_container_width=True):
            move_left()
    with col2:
        if st.button("Jump ⬆️", key="jump", use_container_width=True):
            jump()
    with col3:
        if st.button("Right ➡️", key="right", use_container_width=True):
            move_right()
elif st.session_state.game_over:
    st.markdown(
        f"""
        <div style='text-align: center; margin-top: 100px;'>
            <h2 style='color: #ff5a5f; font-size: 40px;'>GAME OVER</h2>
            <p style='font-size: 24px;'>Final Score: {st.session_state.score}</p>
            <p style='font-size: 24px;'>Level Reached: {st.session_state.level}</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
    if st.button("Play Again", key="reset", use_container_width=True):
        reset_game()
else:
    # Start screen
    st.markdown(
        """
    <div class="instructions">
    <strong>HOW TO PLAY:</strong><br><br>
    ⬅️ Move Left | ➡️ Move Right | ⬆️ Jump<br><br>
    Collect 🪙 coins and 💎 gems to level up!<br>
    Special gems are worth 5 points. Avoid falling!
    </div>
    """,
        unsafe_allow_html=True,
    )
    # COMMENTING FOR NOW
    # st.markdown("""
    #     <div style='text-align: center; margin-top: 50px;'>
    #         <h2 style='color: #ffd700; font-size: 30px;'>Welcome to Retro Pixel Platformer!</h2>
    #         <p style='font-size: 20px; margin-bottom: 30px;'>Collect coins and gems to complete levels</p>
    #         <ul style='text-align: left; max-width: 500px; margin: 0 auto; font-size: 18px;'>
    #             <li>Use Left and Right buttons to move</li>
    #             <li>Press Jump to leap over obstacles</li>
    #             <li>Collect all coins and gems to advance to the next level</li>
    #             <li>Don't fall off the screen!</li>
    #             <li>Special gems are worth 5 points</li>
    #         </ul>
    #     </div>
    # """, unsafe_allow_html=True)

    if st.button("START GAME", key="start", use_container_width=True):
        start_game()

# Footer
st.markdown(
    """
<div class="footer">
  👾 Built with Streamlit | Designed for JAY PARMAR
</div>
""",
    unsafe_allow_html=True,
)
