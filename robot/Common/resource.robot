*** Settings ***
Documentation     A resource file with reusable keywords and variables.
Library           SeleniumLibrary

*** Variables ***
${SERVER}         localhost:5000
${BROWSER}        Chrome
${DELAY}          0
${LOGIN URL}      http://${SERVER}/
${WELCOME URL}    http://${SERVER}/
${NEW USER URL}   http://${SERVER}/new-user
${ERROR URL}      http://${SERVER}/

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    Title Should Be    Grafiki - logowanie

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

Input Username
    [Arguments]    ${username}
    Input Text    username    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    password    ${password}

Submit Credentials
    Click Button    submit

Welcome Page Should Be Open
    Location Should Be    ${WELCOME URL}
    Title Should Be    Grafiki

New User Page Should Be Open
    Location Should Be    ${NEW USER URL}
    Title Should Be    Grafiki - nowy użytkownik

Go To New User Creation
    Go To    ${NEW USER URL}
    Title Should Be    Grafiki - nowy użytkownik

Input New User Username
    [Arguments]    ${new user username}
    Input Text    username    ${new user username}

Input New User Password
    [Arguments]    ${new user password}
    Input Text    password    ${new user password}
    Input Text    password2    ${new user password}

Logout
    Click Link   xpath=//*[@href="/logout"]

Input Current Password
    [Arguments]    ${current password}
    Input Text    old_password    ${current password}

Input New Password
    [Arguments]    ${new password}
    Input Text    new_password1    ${new password}
    Input Text    new_password2    ${new password}

Go To Password Change
    Click Link    change-password
    Title Should Be    Grafiki - zmiana hasła

Check Wrong Login
    Page Should Contain    Nieprawidłowa nazwa użytkownika lub hasło

No User Or Password
    Page Should Contain    Pole wymagane
    
    

