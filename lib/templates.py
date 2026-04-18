"""Small text templates written to disk by the scaffolder.

The two SwiftGen stencils live as plain files under ../stencils/ so they can
be edited without dealing with Python escapes. Only the small bits live here.
"""

SWIFTGEN_YML_TEMPLATE = """strings:
  inputs:
    - "{app}/Supporting files/en.lproj/Localizable.strings"
  outputs:
    - templatePath: "SwiftGen/Scripts/custom-structured-swift5.stencil"
      output: "{app}/Assets/Localization/L10n-Constants.swift"
      params:
        forceFileName: L10n

xcassets:
  inputs:
    - "{app}/Supporting files/Assets.xcassets"
  outputs:
    - templatePath: "SwiftGen/Templates/custom-assets-swiftui.stencil"
      output: "{app}/Assets/Assets-Constants.swift"
      params:
        enumName: Asset
        publicAccess: true
"""


XCASSETS_CONTENTS_JSON = """{
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
"""


LOCALIZABLE_PLACEHOLDER = '/* Localizable.strings — add entries as "key" = "value"; */\n'
