import XMonad
import System.IO
import XMonad.Actions.GroupNavigation
import XMonad.Hooks.SetWMName
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.ManageHelpers
import XMonad.Hooks.RefocusLast
import XMonad.Hooks.InsertPosition
import XMonad.Util.Run(spawnPipe)
import XMonad.Util.SpawnOnce
import XMonad.Util.EZConfig (additionalKeys)
import XMonad.Layout.Tabbed
import XMonad.Layout.NoBorders
import XMonad.Layout.TrackFloating -- Don't go to last tab when floating pops up
import XMonad.Hooks.ManageHelpers
import XMonad.Hooks.Place

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
        , logHook     = refocusLastLogHook
        , handleEventHook = refocusLastWhen myFocusPredicate <+> handleEventHook defaultConfig <+> docksEventHook
        } `additionalKeys` myKeys

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
myLayoutHook  = avoidStruts $ trackFloating(noBorders(tabbed shrinkText myTabConfig)) ||| layoutHook defaultConfig
myFocusPredicate = refocusingIsActive <||> isFloat  -- Return to last tab after closing floating, is definitely necessary combined with trackFloating, I checked
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
myPlacement = withGaps (16,0,16,0) (smart (0.5,0.5)) -- "simpleSmart" is fine too places top-left and down instead of center
myManageHook  = placeHook myPlacement <+> composeAll
    [ 
    isFullscreen --> doFullFloat
    , className =? "Google-chrome"                           --> doShift "3:web"
    , className =? "jetbrains-idea"                          --> doShift "1:code"
    , className =? "Evolution"                               --> doShift "3:web"
    , className =? "Slack"                                   --> doShift "4:admin1"
    , className =? "spotify"                                 --> doShift "4:admin1"
    , className =? "zoom"                                    --> doShift "7"
    , className =? "Pavucontrol"                             --> doShift "7"
    , manageDocks
    ]
myKeys = 
    [ ((0, xK_Print), spawn "maim -s -u | xclip -selection clipboard -t image/png -i") -- 0 means no extra modifier key needs to be pressed in this case.
    , ((myModMask, xK_d), spawn "dmenu_run -i -p \"Run: \"")
    ]

