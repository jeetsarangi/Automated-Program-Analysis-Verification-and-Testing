if (:x + :y > 50) [
    forward :x
    backward :y
] 
if (:x > 20)[
    forward :move
    backward :x
]
if (:move < 50)[
repeat 5 [
	repeat 2 [
		repeat 4 [
			forward :move
			right 45
		]
	]
    ]
]