:y = 90
:x = 180
left :x + :y
backward 45
:y = :x
if :y < :x[
    right 270
]
forward 800
goto(2,2)