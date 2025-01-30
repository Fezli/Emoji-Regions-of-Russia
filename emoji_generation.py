import svgwrite

def generate_emoji_svg(
    filename,
    face_color="#FFD700",
    eye_size=10,
    mouth_shape="neutral",
    brow_shape="neutral",
    bags_shape="none",
    chin_size ="none"
):

    face_opacity=1.0
    parts_color="#282828"
    parts_opacity=0.8

    # Создаем холст SVG
    dwg = svgwrite.Drawing(filename, profile="tiny", size=("100px", "100px"))
    
    # Рисуем лицо (окружность)
    dwg.add(dwg.circle(center=("50", "50"), r="40", fill=face_color, fill_opacity=face_opacity))
    
    # Глаза
    dwg.add(dwg.circle(center=("35", "45"), r=eye_size / 2, fill=parts_color, fill_opacity=parts_opacity))  # Левый глаз
    dwg.add(dwg.circle(center=("65", "45"), r=eye_size / 2, fill=parts_color, fill_opacity=parts_opacity))  # Правый глаз
    
    # Брови
    if brow_shape == "frown":
        # Нахмуренные брови
        dwg.add(dwg.path(
            d="M 25 30 L 40 35", 
            stroke=parts_color, fill="none", stroke_width=2, stroke_opacity=parts_opacity, stroke_linecap="round"))
        dwg.add(dwg.path(
            d="M 75 30 L 60 35", 
            stroke=parts_color, fill="none", stroke_width=2, stroke_opacity=parts_opacity, stroke_linecap="round"))
    elif brow_shape == "neutral":
        # Нейтральные брови
        dwg.add(dwg.path(
            d=f"M 25 35 Q 32 35 40 35", 
            stroke=parts_color, fill="none", stroke_width=2.5, stroke_opacity=parts_opacity, stroke_linecap="round"))
        dwg.add(dwg.path(
            d=f"M 60 35 Q 68 35 75 35", 
            stroke=parts_color, fill="none", stroke_width=2.5, stroke_opacity=parts_opacity, stroke_linecap="round"))
    elif brow_shape == "smile":
        # Расслабленные брови
        dwg.add(dwg.path(
            d="M 25 35 Q 30 25 40 30", 
            stroke=parts_color, fill="none", stroke_width=2, stroke_opacity=parts_opacity, stroke_linecap="round"))
        dwg.add(dwg.path(
            d="M 75 35 Q 71 25 60 30", 
            stroke=parts_color, fill="none", stroke_width=2, stroke_opacity=parts_opacity, stroke_linecap="round"))

    # Мешки под глазами
    if bags_shape in ["light", "dark"]:
        gradient = dwg.defs.add(dwg.linearGradient(
            id="gradient_bags",
            start=(0, 1),  # Снизу
            end=(0, 0)    # Сверху
        ))
        if bags_shape == "light":
            gradient.add_stop_color(offset="0", color="#5b5b5b", opacity=0.2)
            gradient.add_stop_color(offset="100", color="#999999", opacity=0.1)
        elif bags_shape == "dark":
            gradient.add_stop_color(offset="0", color="#444444", opacity=0.3)
            gradient.add_stop_color(offset="100", color="#5b5b5b", opacity=0.2)

        # Левый мешок под глазом
        dwg.add(dwg.path(
            d="M 30 50 Q 35 55 40 50",
            fill="none",
            stroke="url(#gradient_bags)",
            stroke_width=3
        ))

        # Правый мешок под глазом
        dwg.add(dwg.path(
            d="M 60 50 Q 65 55 70 50",
            fill="none",
            stroke="url(#gradient_bags)",
            stroke_width=3
        ))

    # Рот
    if mouth_shape == "smile":
        dwg.add(dwg.path(d="M 70 60 A 20 20 0 0,1 30 60 L 50 60 Z",
            fill=parts_color, fill_opacity=parts_opacity))
    elif mouth_shape == "neutral":
        dwg.add(dwg.line(
            start=("38", "65"), 
            end=("62", "65"), 
            stroke=parts_color, stroke_width=5, stroke_opacity=parts_opacity))
    elif mouth_shape == "sad":
        dwg.add(dwg.path(d="M 70 75 A 20 20 0 0,0 30 75 L 50 75 Z",
            fill=parts_color, fill_opacity=parts_opacity))

    # Подбородок
    if chin_size == "small":
        dwg.add(dwg.path(
            d=f"M 48 87 Q 50 88 52 87", 
            stroke='#5b5b5b', fill="none", stroke_width=1.5, stroke_opacity=0.5, stroke_linecap="round"))
    elif chin_size == "medium":
        dwg.add(dwg.path(
            d=f"M 40 85 Q 50 90 60 85", 
            stroke='#5b5b5b', fill="none", stroke_width=1.5, stroke_opacity=0.5, stroke_linecap="round"))
    elif chin_size == "big":
        dwg.add(dwg.path(
            d=f"M 35 83 Q 50 91 65 83", 
            stroke='#5b5b5b', fill="none", stroke_width=1.5, stroke_opacity=0.5, stroke_linecap="round"))
    
    # Сохраняем результат
    dwg.save()


# Пример использования
generate_emoji_svg(
    filename="emoji_custom.svg",
    face_color="#FFD700", # #FFD700 #EBCD00(#d3b800) #D7C400(#c1b000) #C4BA00(#b0a700)
    eye_size=5, # 2 - 7
    mouth_shape="neutral", # smile neutral sad
    brow_shape="neutral", # smile neutral frown
    bags_shape="none", # none light dark
    chin_size="none" # none small medium big
)
