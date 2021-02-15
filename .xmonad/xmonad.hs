import XMonad
import System.IO
import XMonad.Actions.SpawnOn
import XMonad.Actions.GroupNavigation
import XMonad.Hooks.SetWMName
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.ManageHelpers
import XMonad.Hooks.InsertPosition
import XMonad.Util.Run(spawnPipe)
import XMonad.Util.SpawnOnce
import XMonad.Layout.Tabbed
import XMonad.Layout.NoBorders

import qualified Data.Map as M

main :: IO ()

main = do
    xmonad $ def
        { terminal    = myTerminal
        , modMask     = myModMask
        , borderWidth = myBorderWidth
        , workspaces  = myWorkspaces
        , layoutHook  = myLayoutHook
        , manageHook  = insertPosition End Newer <+> myManageHook
        , startupHook = myStartupHook
        , handleEventHook = handleEventHook defaultConfig <+> docksEventHook
        }

myTerminal    = "urxvt"
myModMask     = mod4Mask
myBorderWidth = 1
myWorkspaces  = ["1:code", "2:comm", "3:web", "4:admin1", "5:admin2", "6", "7", "8", "9", "0"]
myTabConfig = def { activeColor = "#0d0d0d"
                  , inactiveColor = "#000000"
                  , activeBorderColor = "#12bf02"
                  , inactiveBorderColor = "#043d00"
                  , activeTextColor = "#15ff00" -- Strong green
                  , inactiveTextColor = "#15ff00"
                  , fontName = "xft:Source Code Pro Medium:size=10:antialias=true"
                  }
myLayoutHook  = avoidStruts $ noBorders(tabbed shrinkText myTabConfig) ||| layoutHook defaultConfig
myStartupHook = do
    setWMName "LG3D"
    spawnOnce "xmobar"
    spawnOnce "intellij-idea-ultimate-edition"
    spawnOnce "slack"
    spawnOnce "google-chrome-stable"
    spawnOnce "spotify"
    spawnOnce "zoom"
    spawnOnce "pavucontrol"
    spawnOnce "google-chrome-stable"
myManageHook  = composeAll
    [ isFullscreen --> doFullFloat
    , className =? "Google-chrome"                           --> doShift "3:web"
    , className =? "jetbrains-idea"                          --> doShift "1:code"
    , className =? "Evolution"                               --> doShift "3:web"
    , className =? "Slack"                                   --> doShift "4:admin1"
    , className =? "spotify"                                 --> doShift "4:admin1"
    , className =? "zoom"                                    --> doShift "7"
    , className =? "Pavucontrol"                             --> doShift "7"
    , manageDocks
    ]

