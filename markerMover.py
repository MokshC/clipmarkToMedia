#!/usr/bin/env python

# Created by: Moksh Chitkara
# Last Update: Mar 24th 2026
# v0.1.0
# Copyright (C) 2026  Moksh Chitkara
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Global Variables
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
colorLst = ['All','Blue','Cyan','Green','Yellow', 'Red','Pink','Purple','Fuchsia','Rose','Lavender','Sky','Mint','Lemon','Sand','Cocoa','Cream']

################################################################################################
# Window creation #
###################
def main_ui():
	# vertical group
	window = [ui.VGroup({"Spacing": 15,},[
			# horizontal groups
			# Marker Selection
			ui.HGroup({"Spacing": 3}, [ 	
				ui.Label({"ID": "color_label","Text": "Use markers of color: "}),
				ui.ComboBox({"ID": "color_combo"})
			]),
			# Source
			ui.HGroup({"Spacing": 3}, [ 
				ui.Label({"ID": "from_label","Text": "Move markers from: "}),	
				ui.ComboBox({"ID": "from_combo"})
			]),
			# Destination
			ui.HGroup({"Spacing": 3}, [ 
				ui.Label({"ID": "to_label","Text": "Move markers to: "}),	
				ui.ComboBox({"ID": "to_combo"})
			]),
			# Checkbox to delete marker
			ui.HGroup({ 'Weight': 0 }, [
			    ui.VGap(),
			    ui.CheckBox({"ID": "delete_check", "Text": "Delete markers on move", "Checked": True}),
			]),
			# button for export
			ui.Button({"ID": "Start", "Text": "Start Moving!", "Weight": 0}),
			]) 
		]
	return window

ui = fu.UIManager # get UI utility from fusion
disp = bmd.UIDispatcher(ui) # gets display settings?

# window definition
window = disp.AddWindow({"WindowTitle": "Marker Mover",
			"ID": "MMWin", 
			'WindowFlags': {'Window': True,'WindowStaysOnTopHint': True},
			"Geometry": [1500,500,700,250], # x-position, y-position, width, height
			}, 
			main_ui())

itm = window.GetItems() # Grabs all UI elements to be manipulated
################################################################################################
# Functions #
#############

# Given markers and timeline return list of matching clips
# input: markers [dict of markers], timeline [timeline item]
# output: matches [dict of markers]
def get_matches(timeline, track):

    markers = timeline.GetMarkers()
    matches = {}
    # if clip and tl are enabled append start/end to list
    if timeline.GetIsTrackEnabled("video",track):
        print("")
        
        track_items = timeline.GetItemListInTrack("video",track)
        prog = 0
        total = len(track_items)

        for item in track_items:
            prog += 1
            loading = "{:.2%}".format(float(prog)/float(total))
            itm['Start'].Text = "Matching Track {}: {}".format(track, loading)
            if item.GetClipEnabled() and item.GetStart():
                for frame_id in markers:
                    if markers[frame_id]["color"] == str(itm["color_combo"].CurrentText):
                        frame_match = int(frame_id) + int(timeline.GetStartFrame())
                        if (int(item.GetStart()) <= frame_match) and (frame_match < int(item.GetEnd())):
                            print("Match found at", frame_match)
                            matches[frame_match] = markers.pop(frame_id)
                            try:
                                media = item.GetMediaPoolItem()
                            except:
                                media = None
                            matches[frame_match].update({"media": media})
                            break
    return matches


# Apply metadata to clip based on timecode match and delete marker if successful
# input: markers [list of dicts by frame number], starts [list], ends [list], timeline [timeline item], track [int]
# output: None
def apply_meta(matches, timeline, track):


def _main(ev):

    itm['Start'].Enabled = False
    itm['Start'].Text = "Starting..."
    
    timeline = project.GetCurrentTimeline()

    track_range = reversed(range(1, timeline.GetTrackCount("video")+1))
    
    for track in track_range:
        matches = {}
        matches.update(get_matches(timeline, track))
        apply_meta(matches, timeline, track)
        
    itm['Start'].Text = "Move to Metadata"
    itm['Start'].Enabled = True
# needed to close window
def _close(ev):
	disp.ExitLoop()

################################################################################################
# GUI Elements #
# manipulations
itm['from_combo'].AddItems(['Mediapool Clip', 'Timeline Track', 'Timeline Clip']) # adds items to dropdown
itm['to_combo'].AddItems(['Mediapool Clip', 'Timeline Track', 'Timeline Clip']) # adds items to dropdown
itm['color_combo'].AddItems(colorLst)   # adds items to dropdown
# button presses
window.On.Start.Clicked = _main
window.On.MMWin.Close = _close
window.Show()
disp.RunLoop()
window.Hide()
#################################################################################################
