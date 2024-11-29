Get-ChildItem -File -Filter '*.ui' | Foreach {
    $NewName = $_.BaseName + '.py'
    pyside6-uic $_ -o $NewName
}