; This file is part of Qnotero.

; Qnotero is free software: you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation, either version 3 of the License, or
; (at your option) any later version.

; Qnotero is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.

; You should have received a copy of the GNU General Public License
; along with Qnotero.  If not, see <http://www.gnu.org/licenses/>.

; USAGE
; -----
; This script assumes that the binary is located in
; 	E:\PycharmProjects\qnotero\build\exe.win-amd64-3.8
;
; The extension FileAssociation.nsh must be installed. This can be
; done by downloading the script from the link below and copying it
; to a file named FileAssociation.nsh in the Include folder of NSIS.

; For each new release, adjust the PRODUCT_VERSION as follows:
; 	version-win32-package#


; Build Unicode installer
Unicode True

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "Qnotero"
!define PRODUCT_VERSION "2.3.0"
!define PRODUCT_PUBLISHER "E. Albiter"
!define PRODUCT_WEB_SITE "https://github.com/ealbiter/qnotero"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"
!define PRODUCT_BUILD_DIRECTORY "E:\PycharmProjects\qnotero\build\exe.win-amd64-3.8"
!define PRODUCT_RESOURCES_DIRECTORY "E:\PycharmProjects\qnotero\resources"

; MUI 1.67 compatible ------
!include "MUI2.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${PRODUCT_RESOURCES_DIRECTORY}\Windows\qnotero.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "qnotero.exe"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "build\setup-qnotero-${PRODUCT_VERSION}.exe"
InstallDir "$PROGRAMFILES64\Qnotero"
ShowInstDetails hide
ShowUnInstDetails hide

Section "Qnotero" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite try
  File /r "${PRODUCT_BUILD_DIRECTORY}\*.*"
  File "${PRODUCT_BUILD_DIRECTORY}\lib\PyQt5\VCRUNTIME140.dll"
SectionEnd

Section -AdditionalIcons
  CreateDirectory "$SMPROGRAMS\Qnotero"
  CreateShortCut "$SMPROGRAMS\Qnotero\Qnotero.lnk" "$INSTDIR\qnotero.exe" "" "$INSTDIR\qnotero.exe" 0
  CreateShortCut "$SMPROGRAMS\Qnotero\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$SMPROGRAMS\Qnotero\Qnotero.lnk"
  Delete "$SMPROGRAMS\Qnotero\Uninstall.lnk"
  RMDir "$SMPROGRAMS\Qnotero"
  RMDir /r "$INSTDIR"  
  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd