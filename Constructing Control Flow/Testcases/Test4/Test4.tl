:vard = 90
:varf = :vard+89

repeat 90[
   :varc = :varf
   :vara = 78
   :varb = 56
    if :varc != 0 && (:vara < :varb) [
  :varb = 0
]

:varl = (:vara + :varb) * :varc
]

repeat 100[
   :varc = :varf
   :vara = 78
   :varb = 56
    if :varc != 0 && (:vara < :varb) [
  penup
]
pendown
]
