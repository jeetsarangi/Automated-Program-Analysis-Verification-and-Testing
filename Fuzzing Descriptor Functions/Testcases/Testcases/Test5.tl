repeat 5[
    if (:move > :x)[
        repeat 6[
            forward :move
            right 30
            backward :x
        ]
    ]
    else[
        repeat 3[
            forward :x
            right 30
            backward :move
        ]
    ]
]