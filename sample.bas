'  *****  BASIC  *****

FUNCTION PythonScriptEmbeddedInFile(sPythonDef, sPythonFile)
    DIM sURL AS STRING
    DIM sLocationType AS STRING

    'Default return value is Null
    myPythonScript = Null
    ON ERROR GOTO error_exit
    'Specify that "call" is for python functions embedded in this document
    sLocationType = "document"
    'Create a script provider
    scriptProvider = ThisComponent.getScriptProvider()
    'specify this is a script located in the provided filename (
    sURL = "vnd.sun.star.script:" & sPythonFile & "$"
    'specify this is a python file and where is its location
    sURL = sURL & sPythonDef  & "?language=Python&location=" & sLocationType
    myPythonScript = scriptProvider.getScript(sURL)

exit_Function:
    EXIT FUNCTION
error_exit:
    MSGBOX "Error in: myPythonScript: " & Err & ": " & Error$ & " (line : " & Erl & ")"
    GOTO exit_Function
END FUNCTION

FUNCTION SendANumberReturnANumber(exampleParam AS INTEGER) AS INTEGER

    DIM ReturnedProps 'leave undefined

    myscript =  myPythonScript("doubleit", "mypythonfile.py")
    ReturnedValue = myscript.invoke(Array(exampleParam),Array(),Array())

    'if needed make some checks here...
    'IF ReturnedValue = TRUE THEN
    '... do this
    'ELSE
    '... do that
    'END IF

    'return the value
    SendANumberReturnANumber = ReturnedValue

exit_Function:
    EXIT FUNCTION
error_exit:
    MSGBOX "Error in: SendANumberReturnANumber: " & Err & ": " & Error$ & " (line : " & Erl & ")"
    GOTO exit_Function
END FUNCTION

FUNCTION SendManyReturnMany(exampleParam AS INTEGER)
    DIM sParameter1 AS STRING
    DIM iParameter2 AS INTEGER
    DIM ReturnedProps 'leave undefined
    DIM props(1)
    DIM oProperty1 AS NEW com.sun.star.beans.PropertyValue
    DIM oProperty2 AS NEW com.sun.star.beans.PropertyValue

    ON ERROR GOTO error_exit

    'Create a uno property. In python will see it as a tuple
    oProperty1.Name = "dummyname"
    oProperty1.Value = exampleParam

    'Enlist this property to an array. Array will be seen as a python list
    props(0) = oProperty1

    oProperty2.Name = "dummy2name"
    oProperty2.Value = "A string value for property 2"

    'Enlist this property to an array. Array will be seen as a python list
    props(1) = oProperty2

    sParameter1 = "some string"
    iParameter2 = 10

    myscript =  myPythonScript("acomplicatedparadigm", "mypythonfile.py")
    'python script will receive a tuple
    'the first member will be also a tuple, containing 2 members of type: PropertyValue
    'so you must:
    'import uno
    'from com.sun.star.beans import PropertyValue

    ReturnedValues = myscript.invoke(Array(props(), sParameter1, iParameter2),Array(),Array())
    'python cannot return a list or dict
    'you must return a tuple which will be seen as array here
    SendManyReturnMany = ReturnedValues


exit_Function:
    EXIT FUNCTION
error_exit:
    MSGBOX "Error in: SendManyReturnMany: " & Err & ": " & Error$ & " (line : " & Erl & ")"
    GOTO exit_Function
END FUNCTION
