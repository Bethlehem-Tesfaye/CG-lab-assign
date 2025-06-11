from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import sqrt, cos, sin, pi

window_size = 600

drawing = False
current_color = [0.0, 0.0, 0.0]
draw_mode = "line"  

strokes = []  
current_stroke = []

circles = []
circle_start = None
circle_radius = 0

ui_buttons = {
    "red":    (10, 10, 60, 40),
    "green":  (70, 10, 120, 40),
    "blue":   (130, 10, 180, 40),
    "clear":  (200, 10, 270, 40),
    "line":   (280, 10, 330, 40),
    "circle": (340, 10, 410, 40)
}

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_12):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

def is_inside(x, y, rect):
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2

def display():
    glClear(GL_COLOR_BUFFER_BIT)


    for name, (x1, y1, x2, y2) in ui_buttons.items():
       
        if name == "red":
            glColor3f(1, 0, 0)
        elif name == "green":
            glColor3f(0, 1, 0)
        elif name == "blue":
            glColor3f(0, 0, 1)
        elif name == "clear":
            glColor3f(0.8, 0.8, 0.8)
        elif name == "line":
            glColor3f(0.6, 0.6, 0.6) if draw_mode != "line" else glColor3f(0.3, 0.3, 0.3)
        elif name == "circle":
            glColor3f(0.6, 0.6, 0.6) if draw_mode != "circle" else glColor3f(0.3, 0.3, 0.3)

        glBegin(GL_QUADS)
        glVertex2f(x1, y1)
        glVertex2f(x2, y1)
        glVertex2f(x2, y2)
        glVertex2f(x1, y2)
        glEnd()

        
        glColor3f(0, 0, 0)
        label = name.capitalize() if name != "clear" else "Clear"
        draw_text(x1 + 5, y1 + 15, label)

    for stroke in strokes:
        if len(stroke) < 2:
            continue
        glBegin(GL_LINE_STRIP)
        for (x, y, color) in stroke:
            glColor3f(*color)
            glVertex2f(x, y)
        glEnd()

    if draw_mode == "line" and drawing and len(current_stroke) >= 2:
        glBegin(GL_LINE_STRIP)
        for (x, y, color) in current_stroke:
            glColor3f(*color)
            glVertex2f(x, y)
        glEnd()

    for (cx, cy, r, color) in circles:
        glColor3f(*color)
        draw_circle_outline(cx, cy, r)

    if draw_mode == "circle" and drawing and circle_start is not None:
        glColor3f(*current_color)
        draw_circle_outline(circle_start[0], circle_start[1], circle_radius)

    glutSwapBuffers()

def draw_circle_outline(cx, cy, radius):
    glBegin(GL_LINE_LOOP)
    for i in range(100):
        angle = 2 * pi * i / 100
        x = cx + radius * cos(angle)
        y = cy + radius * sin(angle)
        glVertex2f(x, y)
    glEnd()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_size, window_size, 0)
    glMatrixMode(GL_MODELVIEW)

def mouse(button, state, x, y):
    global drawing, current_color, current_stroke, strokes
    global circle_start, circle_radius, circles, draw_mode

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            for name, rect in ui_buttons.items():
                if is_inside(x, y, rect):
                    if name == "red":
                        current_color[:] = [1, 0, 0]
                    elif name == "green":
                        current_color[:] = [0, 1, 0]
                    elif name == "blue":
                        current_color[:] = [0, 0, 1]
                    elif name == "clear":
                        strokes.clear()
                        circles.clear()
                    elif name == "line":
                        draw_mode = "line"
                    elif name == "circle":
                        draw_mode = "circle"
                    glutPostRedisplay()
                    return

            drawing = True

            if draw_mode == "line":
                current_stroke = [(x, y, current_color[:])]
            elif draw_mode == "circle":
                circle_start = (x, y)
                circle_radius = 0

        elif state == GLUT_UP:
            drawing = False
            if draw_mode == "line":
                if current_stroke:
                    strokes.append(current_stroke)
                    current_stroke = []
            elif draw_mode == "circle":
                if circle_start is not None and circle_radius > 0:
                    circles.append((circle_start[0], circle_start[1], circle_radius, current_color[:]))
                circle_start = None
                circle_radius = 0
    glutPostRedisplay()

def motion(x, y):
    global current_stroke, circle_radius

    if not drawing:
        return

    if draw_mode == "line":
        current_stroke.append((x, y, current_color[:]))
    elif draw_mode == "circle" and circle_start is not None:
        dx = x - circle_start[0]
        dy = y - circle_start[1]
        circle_radius = sqrt(dx*dx + dy*dy)

    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_size, window_size)
    glutCreateWindow(b"Paint-like Drawing: Lines and Circles")
    glClearColor(1, 1, 1, 1)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutMainLoop()

if __name__ == "__main__":
    main()
