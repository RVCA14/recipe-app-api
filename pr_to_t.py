test_str = 'Te informamos que se ha realizado una compra por $5.987 con Tarjeta de Crédito ****1356 en UBER LAS CONDES CL el 03/11/2022 21:10. Revisa Saldos y Movimientos en App Mi Banco o Banco en Línea.'

print(test_str)

sub1 = "por "
sub2 = " con"
# getting index of substrings
idx1 = test_str.index(sub1)
idx2 = test_str.index(sub2)
res = ''
# getting elements in between
for idx in range(idx1 + len(sub1) , idx2):
    res = res + test_str[idx]
# printing result
res = res.replace("$","").replace(".","")
expense = int(res)
print("Expense is:", expense)

sub1 = "con "
sub2 = " en"

# getting index of substrings
idx1 = test_str.index(sub1)
idx2 = test_str.index(sub2)

res = ''
# getting elements in between
for idx in range(idx1 + len(sub1) , idx2):
    res = res + test_str[idx]

card = res
# printing result
print("Card : " + res)

sub1 = "en "
sub2 = " el"
# getting index of substrings
idx1 = test_str.index(sub1)
idx2 = test_str.index(sub2)
res = ''
# getting elements in between
for idx in range(idx1 + len(sub1) , idx2):
    res = res + test_str[idx]
# printing result
supplier = res
print("Supplier: " + res)


sub1 = "el "
sub2 = ". "

# getting index of substrings
idx1 = test_str.index(sub1)
idx2 = test_str.index(sub2)

res = ''
# getting elements in between
for idx in range(idx1 + len(sub1) , idx2):
    res = res + test_str[idx]
date = res
# printing result
print("Date: " + res)

diccionario = {
    'expense': expense,
    'card': card,
    'supplier': supplier,
    'date': date
}
print(diccionario)