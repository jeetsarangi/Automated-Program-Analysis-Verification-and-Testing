:vara = 90
:varb = 78
:varc = 67
:vard = 45

if :vara > :varb && :varc == :vard[
repeat 100[
   :varc = :varf
   :vara = 78
   :varb = 56
    if :varc != 0 && (:vara < :varb) [
  penup
]
pendown
]

repeat 10 [  
      :vark = :vara + :varb
      :varj = :varc * :vard
      if :vark >= :varj[
      repeat 10 [
         :vara = 0
         :varb = 0
      ]
      ]
   ]
]