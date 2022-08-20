right :x
if (:x + :z < 50)[
    forward :x + :z
]

else[
forward 20
]

repeat 5[
    :x = :x+5
    repeat 3[
    forward :x
    right 90
    ]
]