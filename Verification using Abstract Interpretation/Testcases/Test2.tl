:x = 1
:y = :x + 3
forward 200
right 90
left 180
backward 20
:x = :x + 89
if :x > 10[
    left 180
]
backward 60
forward 200
right 90
if (:x + :y) < 100[
    forward 80
] 
