import XMonad
import System.IO
import XMonad.Hooks.SetWMName
import XMonad.Actions.SpawnOn
import XMonad.Hooks.ManageDocks
import XMonad.Util.Run(spawnPipe)
import XMonad.Util.SpawnOnce

import qualified Data.Map as M

main :: IO ()

main = do
  xmonad $ defaultConfig
    { terminal    = myTerminal
    , modMask     = myModMask
    , borderWidth = myBorderWidth
    , workspaces  = myWorkspaces
    , layoutHook  = avoidStruts $ layoutHook defaultConfig
    , manageHook  = myManageHook <+> manageHook defaultConfig
    , startupHook = myStartupHook
    , handleEventHook = handleEventHook defaultConfig <+> docksEventHook
    }

myTerminal    = "urxvt"
myModMask     = mod4Mask
myBorderWidth = 1
myWorkspaces  = ["1:code", "2:comm", "3:web", "4:admin1", "5:admin2", "6", "7", "8", "9", "0"]
myManageHook  = composeAll
    [ className =? "Google-chrome"                           --> doShift "3:web"
    , className =? "jetbrains-idea"                          --> doShift "1:code"
    , className =? "Evolution"                               --> doShift "3:web"
    , className =? "Slack"                                   --> doShift "4:admin1"
    , className =? "Spotify"                                 --> doShift "4:admin1"
    , className =? "Pavucontrol"                             --> doShift "7"
    , className =? "zoom"                                    --> doShift "7"
    , manageDocks
    ]
myStartupHook = do 
  setWMName "LG3D"
