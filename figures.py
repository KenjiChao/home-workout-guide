# -*- coding: utf-8 -*-
"""Programmatic stick-figure generator for the home-workout guide.
Each exercise renders a single SVG showing START pose (ghost) -> END pose (solid amber)
with a motion arrow. Side-profile view, consistent skeleton, whiskey-amber on dark leather.
"""
import math

# Palette
AMBER = "#E0A144"     # end pose (the working position)
GHOST = "#6E5B45"     # start pose (muted)
ARROW = "#EBC98A"     # motion arrow
VB_W, VB_H = 240, 200
GROUND = 186

def _line(p1, p2, color, w, op=1.0):
    return (f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>')

def _circle(c, r, color, w, fill="none", op=1.0):
    return (f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r}" stroke="{color}" '
            f'stroke-width="{w}" fill="{fill}" opacity="{op}"/>')

def figure(P, color, w, headfill="none", op=1.0):
    """Render one stick figure from a joint dict P."""
    s = []
    # head
    s.append(_circle(P['head'], P.get('hr', 11), color, w, fill=(color if headfill=="solid" else "none"), op=op))
    # neck
    s.append(_line(P['head'], P['shoulder'], color, w, op))
    # torso
    s.append(_line(P['shoulder'], P['hip'], color, w, op))
    # front arm
    s.append(_line(P['shoulder'], P['elbow'], color, w, op))
    s.append(_line(P['elbow'], P['hand'], color, w, op))
    # back arm (optional)
    if 'elbowB' in P:
        s.append(_line(P['shoulder'], P['elbowB'], color, w*0.85, op*0.75))
        s.append(_line(P['elbowB'], P['handB'], color, w*0.85, op*0.75))
    # front leg
    s.append(_line(P['hip'], P['knee'], color, w, op))
    s.append(_line(P['knee'], P['foot'], color, w, op))
    # back leg (optional)
    if 'kneeB' in P:
        s.append(_line(P['hip'], P['kneeB'], color, w*0.85, op*0.75))
        s.append(_line(P['kneeB'], P['footB'], color, w*0.85, op*0.75))
    return "".join(s)

def arrow(x1, y1, x2, y2, curve=0):
    """Straight-ish motion arrow with a head."""
    ang = math.atan2(y2 - y1, x2 - x1)
    ah = 7
    a1 = (x2 - ah*math.cos(ang - 0.5), y2 - ah*math.sin(ang - 0.5))
    a2 = (x2 - ah*math.cos(ang + 0.5), y2 - ah*math.sin(ang + 0.5))
    if curve:
        mx, my = (x1+x2)/2 + curve, (y1+y2)/2
        path = f'<path d="M{x1:.1f},{y1:.1f} Q{mx:.1f},{my:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="{ARROW}" stroke-width="3" stroke-linecap="round"/>'
    else:
        path = _line((x1,y1),(x2,y2), ARROW, 3)
    head = (f'<polygon points="{x2:.1f},{y2:.1f} {a1[0]:.1f},{a1[1]:.1f} {a2[0]:.1f},{a2[1]:.1f}" fill="{ARROW}"/>')
    return path + head

def svg(start, end, arrows, ground=True):
    parts = [f'<svg viewBox="0 0 {VB_W} {VB_H}" xmlns="http://www.w3.org/2000/svg" class="fig">']
    if ground:
        parts.append(f'<line x1="20" y1="{GROUND}" x2="{VB_W-20}" y2="{GROUND}" stroke="#3a3128" stroke-width="3" stroke-linecap="round"/>')
    parts.append(figure(start, GHOST, 5, headfill="none", op=0.85))
    parts.append(figure(end, AMBER, 7, headfill="solid", op=1.0))
    for a in arrows:
        parts.append(arrow(*a[:4], curve=a[4] if len(a)>4 else 0))
    parts.append('</svg>')
    return "".join(parts)
