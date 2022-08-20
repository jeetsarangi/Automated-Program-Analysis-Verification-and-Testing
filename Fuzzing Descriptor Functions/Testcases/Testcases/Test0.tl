if (:x > :y - 6)[
    repeat 3[
        right 120
        forward :z
    ]
]
forward 10
repeat 3[
    right 120
    forward :y
]
if (:x > :y + :z)[
    repeat 6[
        right 120
        forward :z
        forward 7
    ]
]
