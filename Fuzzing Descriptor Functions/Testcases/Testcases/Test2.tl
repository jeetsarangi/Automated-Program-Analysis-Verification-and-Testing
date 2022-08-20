forward :z
if (:x > :y)[
    repeat 3[
        right 120
        forward :z
    ]
]
else[
    repeat 6[
        left 30
        forward :y
    ]
]
forward 40
if (:x > 10)[
repeat 6[
        left 30
        forward :y
    ]
    ]