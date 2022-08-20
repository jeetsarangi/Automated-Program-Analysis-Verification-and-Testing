:varb = 20
:vara = :varb

if :vara == :varb [
   :vara = 0
   :varb = 0	
   
   if :vara < :varb [
   :vara = 0
   :varb = 0
]

if :vara < :varb || :vara == :varb [
   :vara = 0
   :varb = -5 + 10
]

if :vara > :varb [
   :vara = 90
   :varb = 100
   :varc = 78
   :varf = 77
]
]

penup