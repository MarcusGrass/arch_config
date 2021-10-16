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
import XMonad.Layout.MultiToggle.Instances (StdTransformers(NBFULL, MIRROR, NOBORDERS))
import XMonad.Hooks.EwmhDesktops  -- for some fullscreen events, also for xcomposite in obs.
import XMonad.Hooks.ManageHelpers
import XMonad.Hooks.Place
import XMonad.Hooks.DynamicLog (dynamicLogWithPP, wrap, xmobarPP, xmobarColor, shorten, PP(..))
import XMonad.Hooks.DynamicProperty
import XMonad.Util.NamedScratchpad

import Data.Maybe (fromJust)
import qualified Data.Map as M
import qualified XMonad.StackSet as W
import qualified XMonad.Layout.MultiToggle as MT (Toggle(..))

main :: IO ()

main = do
    xmproc0 <- spawnPipe "xmobar -x 0 $HOME/.config/xmobar/xmobarrc"
    xmproc1 <- spawnPipe "xmobar -x 1 $HOME/.config/xmobar/xmobarrc"
    xmproc2 <- spawnPipe "xmobar -x 2 $HOME/.config/xmobar/xmobarrc"
    xmproc3 <- spawnPipe "xmobar -x 3 $HOME/.config/xmobar/xmobarrc"
    xmonad $ ewmh def
        { terminal    = myTerminal
        , modMask     = myModMask
        , borderWidth = myBorderWidth
        , normalBorderColor  = myNormColor
        , focusedBorderColor = myFocusColor
        , workspaces  = myWorkspaces
        , layoutHook  = refocusLastLayoutHook $ myLayoutHook
        , manageHook  = insertPosition End Newer <+> myManageHook
        , startupHook = myStartupHook
        , handleEventHook = refocusLastWhen myFocusPredicate <+> handleEventHook defaultConfig <+> docksEventHook <+> dynamicPropertyChange "WM_NAME" (title =? "Spotify" --> doShift "mus")
        , logHook     = dynamicLogWithPP $ xmobarPP
              -- the following variables beginning with 'pp' are settings for xmobar.
              { ppOutput = \x -> hPutStrLn xmproc0 x                          -- xmobar on monitor 1
                              >> hPutStrLn xmproc1 x                          -- xmobar on monitor 2
                              >> hPutStrLn xmproc2 x                          -- xmobar on monitor 3
                              >> hPutStrLn xmproc3 x                          -- xmobar on monitor 4
              , ppCurrent = xmobarColor "#c792ea" "" . wrap "<box type=Bottom width=2 mb=2 color=#c792ea>" "</box>"         -- Current workspace
              , ppVisible = xmobarColor "#c792ea" "" . clickable                          -- Visible but not current workspace
              , ppHidden = xmobarColor "#82AAFF" "" . wrap "<box type=Top width=2 mt=2 color=#82AAFF>" "</box>" . clickable -- Hidden workspaces
              , ppHiddenNoWindows = xmobarColor "#82AAFF" "" -- Hidden workspaces (no windows)
              , ppTitle = xmobarColor "#82AAFF" "" . shorten 60               -- Title of active window
              , ppSep =  "<fc=#666666> <fn=1>|</fn> </fc>"                    -- Separator character
              , ppUrgent = xmobarColor "#C45500" "" . wrap "!" "!"            -- Urgent workspace
              --, ppExtras  = [windowCount]                                     -- # of windows current workspace
              , ppOrder  = \(ws:l:t:ex) -> [ws]++ex++[t]                    -- order of things in xmobar
              }
        } `additionalKeys` myKeys

clickable ws = "<action=xdotool key super+"++show i++">"++ws++"</action>"
    where i = fromJust $ M.lookup ws myWorkspaceIndices

myNormColor :: String
myNormColor   = "#282c34"   -- Border color of normal windows
myFocusColor :: String
myFocusColor  = "#82AAFF"   -- Border color of focused windows
windowCount :: X (Maybe String)
windowCount = gets $ Just . show . length . W.integrate' . W.stack . W.workspace . W.current . windowset

myTerminal    = "alacritty"
myModMask     = mod4Mask
myBorderWidth = 1
-- myWorkspaces = [" 1 ", " 2 ", " 3 ", " 4 ", " 5 ", " 6 ", " 7 ", " 8 ", " 9 "]
myWorkspaces  = ["dev", "term", "web", "com", "mus", "mc1", "sys", "mc2", "mc3"]
myWorkspaceIndices = M.fromList $ zipWith (,) myWorkspaces [1..] -- (,) == \x y -> (x,y)
myTabConfig = def { activeColor         = "#82AAFF"
                  , inactiveColor       = "#313846"
                  , activeBorderColor   = "#82AAFF"
                  , inactiveBorderColor = "#282c34"
                  , activeTextColor     = "#282c34"
                  , inactiveTextColor   = "#d0d0d0"                  
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
    spawnOnce "pavucontrol"
    spawnOnce "google-chrome-stable"
    spawnOnce "discord"
myPlacement = withGaps (16,0,16,0) (smart (0.5,0.5)) -- "simpleSmart" is fine too places top-left and down instead of center
myManageHook  = placeHook myPlacement <+> composeAll
    [ 
    isFullscreen --> doFullFloat
    , className =? "Google-chrome"                           --> doShift "web"
    , className =? "jetbrains-idea"                          --> doShift "dev"
    , className =? "Evolution"                               --> doShift "com"
    , className =? "Slack"                                   --> doShift "com"
    , className =? "spotify"                                 --> doShift "mus"
    , className =? "discord"                                 --> doShift "com"
    , className =? "Pavucontrol"                             --> doShift "sys"
    , manageDocks
    ]
myKeys = 
    [ ((0, xK_Print), spawn "maim -s -u | xclip -selection clipboard -t image/png -i") -- 0 means no extra modifier key needs to be pressed in this case.
    , ((myModMask, xK_d), spawn "dmenu_run -i -p \"Run: \"")
    , ((myModMask, xK_b), sendMessage (MT.Toggle NBFULL) >> sendMessage ToggleStruts) -- Toggles noborder/full
    ]

