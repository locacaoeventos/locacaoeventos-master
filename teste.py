x = "52998224725"
sum_tot = 0
for i in range(1,10):
    sum_tot += int(x[i-1])*(11-i)
    print(int(x[i-1])*(11-i))
dig1 = str((sum_tot*10)%11)
if dig1 == '10':
    dig1 = '0'
sum_tot = 0
for i in range(1,11):
    sum_tot += int(x[i-1])*(12-i)
    print(int(x[i-1])*(12-i))
dig2 = str((sum_tot*10)%11)
if dig2 == '10':
    dig2 = '0'
print(dig1)
print(dig2)

