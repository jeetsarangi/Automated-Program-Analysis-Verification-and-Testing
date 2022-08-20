:x = 1100
:y = 2000
penup 
:y1 = :x + 20 
if (:y1 > 42) [ 
  :y2 = :z - 20
  :t = :y1 + :y2
forward :t
] else [ 
  :y2 = :w - 20
  :t = :y1 + :y2
  forward :t
] 
pendown