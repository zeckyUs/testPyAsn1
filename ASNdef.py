from pyasn1.type import univ, namedtype, constraint, error
from pyasn1.type import char
from pyasn1.codec.der import encoder, decoder

'''
Asn1Def DEFINITIONS AUTOMATIC TAGS ::=
BEGIN
  CasinoPlayer ::= SEQUENCE
  {
     name      UTF8String (SIZE(1..16)),
     luckyNumbers SEQUENCE  (SIZE(3)) OF INTEGER DEFAULT {7,7,7}
  }
END
'''

class CasinoPlayer(univ.Sequence):

    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'name',
            char.UTF8String(
                constraint.ConstraintsIntersection(
                    constraint.ValueSizeConstraint(1, 16)
                )
            )
        ),
        namedtype.DefaultedNamedType(
            'luckyNumbers',
            univ.SequenceOf(
                componentType=univ.Integer(),
                sizeSpec=constraint.ConstraintsIntersection(
                    constraint.ValueSizeConstraint(3, 3)
                )
            ).setComponentByPosition(0, 7)
             .setComponentByPosition(1, 7)
             .setComponentByPosition(2, 7)
        )
    )

def encode():

    # Test 1: Encode with internal objects instantiated and default values
    luckyPlayer = CasinoPlayer()
    luckyPlayer.setComponentByName('name', 'lucky')

    luckyNum = luckyPlayer.getComponentByName('luckyNumbers')
    luckyNum.setComponentByPosition(0, 7)
    luckyNum.setComponentByPosition(1, 7)
    luckyNum.setComponentByPosition(2, 7)

    luckyEncoded = encoder.encode(luckyPlayer)

    print("Test1 - Encoded: " + luckyEncoded.hex())
    assert luckyEncoded.hex() == "30070c056c75636b79"

    # Test 2: Encode with internal objects instantiated and non default values
    luckyPlayer = CasinoPlayer()
    luckyPlayer.setComponentByName('name', 'lucky')

    luckyNum = luckyPlayer.getComponentByName('luckyNumbers')
    luckyNum.setComponentByPosition(0, 6)
    luckyNum.setComponentByPosition(1, 6)
    luckyNum.setComponentByPosition(2, 6)

    luckyEncoded = encoder.encode(luckyPlayer)

    print("Test2 - Encoded: " + luckyEncoded.hex())
    assert luckyEncoded.hex() == "30120c056c75636b793009020106020106020106"

    # Test 3: Encode with internal objects instantiated and setting 2 values instead of 3
    luckyPlayer = CasinoPlayer()
    luckyPlayer.setComponentByName('name', 'lucky')

    luckyNum = luckyPlayer.getComponentByName('luckyNumbers')
    luckyNum.setComponentByPosition(0, 6)
    luckyNum.setComponentByPosition(1, 6)

    luckyEncoded = encoder.encode(luckyPlayer)

    print("TO BE CHECKED: Test3 - Encoded: " + luckyEncoded.hex())

    #TODO: Is it supposed to work as only 2 values, non default are set?
    assert luckyEncoded.hex() == "30120c056c75636b793009020106020106020107"

    # Test 4: Encode with internal objects instantiated and setting 4 values instead of 3
    luckyPlayer = CasinoPlayer()
    luckyPlayer.setComponentByName('name', 'lucky')

    luckyNum = luckyPlayer.getComponentByName('luckyNumbers')
    luckyNum.setComponentByPosition(0, 6)
    luckyNum.setComponentByPosition(1, 6)
    luckyNum.setComponentByPosition(2, 6)
    luckyNum.setComponentByPosition(3, 6)

    try:
        luckyEncoded = encoder.encode(luckyPlayer)
        raise ValueError

    except error.ValueConstraintError:
        print("Test4 - Encoding failed as expected due to the size constraint")

    # Test 5: Encode with objects allocated using default values
    luckyPlayer = CasinoPlayer()
    luckyPlayer.setComponentByName('name', 'lucky')

    luckyNumbers = univ.SequenceOf(componentType=univ.Integer())
    luckyNumbers.setComponentByPosition(0, 7)
    luckyNumbers.setComponentByPosition(1, 7)
    luckyNumbers.setComponentByPosition(2, 7)
    luckyPlayer.setComponentByName('luckyNumbers', luckyNumbers)

    luckyEncoded = encoder.encode(luckyPlayer)

    print("Test5 - Encoded: " + luckyEncoded.hex())

    assert luckyEncoded.hex() == "30070c056c75636b79"

    # Test 6: Encode with objects allocated using non default values
    luckyPlayer = CasinoPlayer()
    luckyPlayer.setComponentByName('name', 'lucky')

    luckyNumbers = univ.SequenceOf(componentType=univ.Integer())
    luckyNumbers.setComponentByPosition(0, 5)
    luckyNumbers.setComponentByPosition(1, 7)
    luckyNumbers.setComponentByPosition(2, 3)
    luckyPlayer.setComponentByName('luckyNumbers', luckyNumbers)

    luckyEncoded = encoder.encode(luckyPlayer)

    print("Test6 - Encoded: " + luckyEncoded.hex())

    assert luckyEncoded.hex() == "30120c056c75636b793009020105020107020103"

    # Test 7: Encode with objects allocated having 2 fields
    luckyPlayer = CasinoPlayer()
    luckyPlayer.setComponentByName('name', 'lucky')

    luckyNumbers = univ.SequenceOf(componentType=univ.Integer())
    luckyNumbers.setComponentByPosition(0, 5)
    luckyNumbers.setComponentByPosition(1, 7)
    luckyPlayer.setComponentByName('luckyNumbers', luckyNumbers)

    try:
        luckyEncoded = encoder.encode(luckyPlayer)
        raise ValueError("Test 7 - Expected to fail but is working, encoding is " + luckyEncoded.hex())

    except error.ValueConstraintError:
        print("Test7 - Encoding failed as expected due to the size constraint")

    # Test 8: Encode with objects allocated having 4 fields
    luckyPlayer = CasinoPlayer()
    luckyPlayer.setComponentByName('name', 'lucky')

    luckyNumbers = univ.SequenceOf(componentType=univ.Integer())
    luckyNumbers.setComponentByPosition(0, 5)
    luckyNumbers.setComponentByPosition(1, 7)
    luckyNumbers.setComponentByPosition(2, 7)
    luckyNumbers.setComponentByPosition(3, 8)

    luckyPlayer.setComponentByName('luckyNumbers', luckyNumbers)

    try:
        luckyEncoded = encoder.encode(luckyPlayer)
        raise ValueError("Test 8 - Expected to fail but is working, encoding is " + luckyEncoded.hex())

    except error.ValueConstraintError:
        print("Test8 - Encoding failed as expected due to the size constraint")

def decode():

    #substrate = '300f0c056c75636b793006020107020107'
    substrate = '30070c056c75636b79'
    substrate = bytes.fromhex(substrate)

    luckyPlayer = decoder.decode(substrate, asn1Spec=CasinoPlayer())[0]

    print(luckyPlayer.prettyPrint())

    name = luckyPlayer.getComponentByName('name')
    print(name)

    luckyNumbers = luckyPlayer.getComponentByName('luckyNumbers')
    print(type(luckyNumbers))

    num1 = luckyNumbers.getComponentByPosition(0)
    num2 = luckyNumbers.getComponentByPosition(1)
    num3 = luckyNumbers.getComponentByPosition(2)

    print(type(num1))

if __name__ == '__main__':
    encode()
