# Spirent TestCenter Logic Script
# Generated on Mon Jan 05 11:56:15 2015 by udayakum
# Framework ver. 3.60.7966.0000
#
# Comments: 
# 
#
# This logic script contains the following routines invoked from the
# stc_100mb_p1_rand_100L.tcl script.

# Load Spirent TestCenter
package require SpirentTestCenter
#source SpirentTestCenter.tcl

#    init - set the logging level and logging location (stdout).
#           Possible logLevel values are: 
#             DEBUG - Display DEBUG, INFO, WARN, and ERROR messages
#             INFO  - Display INFO, WARN, and ERROR messages
#             WARN  - Display WARN and ERROR messages
#             ERROR - Display only ERROR messages
#
#           Possible values for logTo are "stdout" or a file name (can include
#           the path). Use forward slashes between directory names.
proc init {} {
    stc::config automationoptions -logTo stdout -logLevel WARN
}

#    configResultLocation -  set the location for results files.
#            Possible values are: 
#              INSTALL_DIR - Spirent TestCenter installation directory.
#              CURRENT_WORKING_DIR - Current working directory. This 
#                  is the directory that Spirent TestCenter currently
#                  has open.
#              USER_WORKING_DIR - User working directory.
#              CURRENT_CONFIG_DIR - Current configuration directory. 
#                  This is the directory where the saved or loaded
#                  .xml or .tcc file is located. If no .xml or .tcc 
#                  file has been saved or loaded, files are saved
#                  to the user working directory.
#
#            The location of the results files can be modified in the
#            launcher file. The saveResultsRelativeTo parameter sets a path 
#            that is prepended to the value of the ResultsDirectory 
#            parameter. To set an fully qualified (absolute) path for 
#            results, set the ResultsDirectory parameter and set 
#            SaveResultsRelativeTo to NONE.
proc configResultLocation  { location } {
    set TestResultSetting(1) [lindex [stc::get System1.Project -children-TestResultSetting] 0]
    stc::config $TestResultSetting(1) -saveResultsRelativeTo NONE -resultsDirectory $location
}

#    configMiscOptions - set up the sequencer. Currently sets the sequencer
#                        to stop on any error.  Other options are IGNORE_ERROR and 
#                        PAUSE_ON_ERROR.
proc configMiscOptions  {} {
    set Sequencer(1) [lindex [stc::get system1 -children-sequencer] 0]
    stc::config $Sequencer(1) -ErrorHandler STOP_ON_ERROR
}

#    config - load the configuration into memory. The port locations
#             are taken from the XML file and are not passed in from the
#             launcher script.
proc config {ports} {

set StcSystem(1) [ stc::perform loadfromxml -filename [ file join [ file dirname [ info script ] ] {stc_100mb_p1_rand_100L.xml} ] ]

    # Save to an XML file, if desired
    #stc::perform saveAsXml -config system1 -filename sampleSavedFilename.xml
    
    # Save to a Tcl file, if desired
    #stc::perform saveAsTcl -config system1 -filename sampleSavedFilename.tcl

}

#    connect - perform the logical to physical port mapping, connect to the 
#              chassis' and reserve the ports. This routine performs the connect,
#              reserve, and logical to physical port mappings directly.
#              The port list is retrieved from the in-memory configuration.
proc connect {} {
    stc::perform attachPorts -autoConnect true -portList [ stc::get project1 -children-Port ]
}

#    apply - apply writes the logical information held in memory on the 
#            workstation to the ports in the STC chassis'.
proc apply {} {
    stc::apply
}

#    run - subscribe to any results views located in the in-memory configuration
#          and execute the sequencer and return the test status from the 
#          command sequence, if any. Test status is set by the Stopped Reason
#          in the Stop Command Sequence command. This is a string value and 
#          can be anything. If there is no sequence defined or no Stop 
#          Command Sequence command is executed, then the test state is 
#          returned. Test state can take the values: NONE, PASSED or FAILED.
proc run {} {
    # Subscribe to results for result query stc_100mb_p1_rand_100L-0001-generatorportresults
    stc::subscribe -parent [lindex [stc::get system1 -children-Project] 0] \
        -resultParent " [lindex [stc::get system1 -children-Project] 0] " \
        -configType generator \
        -resultType generatorportresults \
        -filterList "" \
        -viewAttributeList "totalframecount totaloctetcount generatorframecount generatoroctetcount generatorsigframecount generatorundersizeframecount generatoroversizeframecount generatorjumboframecount totalframerate totaloctetrate generatorframerate generatoroctetrate generatorsigframerate generatorundersizeframerate generatoroversizeframerate generatorjumboframerate generatorcrcerrorframecount generatorl3checksumerrorcount generatorl4checksumerrorcount generatorcrcerrorframerate generatorl3checksumerrorrate generatorl4checksumerrorrate totalipv4framecount totalipv6framecount totalmplsframecount generatoripv4framecount generatoripv6framecount generatorvlanframecount generatormplsframecount totalipv4framerate totalipv6framerate totalmplsframerate generatoripv4framerate generatoripv6framerate generatorvlanframerate generatormplsframerate totalbitrate generatorbitrate l1bitcount l1bitrate pfcframecount pfcpri0framecount pfcpri1framecount pfcpri2framecount pfcpri3framecount pfcpri4framecount pfcpri5framecount pfcpri6framecount pfcpri7framecount " \
        -interval 1 -filenamePrefix "stc_100mb_p1_rand_100L-0001-generatorportresults"

    # Subscribe to results for result query stc_100mb_p1_rand_100L-0002-analyzerportresults
    stc::subscribe -parent [lindex [stc::get system1 -children-Project] 0] \
        -resultParent " [lindex [stc::get system1 -children-Project] 0] " \
        -configType analyzer \
        -resultType analyzerportresults \
        -filterList "" \
        -viewAttributeList "totalframecount totaloctetcount sigframecount undersizeframecount oversizeframecount jumboframecount minframelength maxframelength pauseframecount totalframerate totaloctetrate sigframerate undersizeframerate oversizeframerate jumboframerate pauseframerate fcserrorframecount ipv4checksumerrorcount tcpchecksumerrorcount udpchecksumerrorcount prbsfilloctetcount prbsbiterrorcount fcserrorframerate ipv4checksumerrorrate tcpchecksumerrorrate udpchecksumerrorrate prbsfilloctetrate prbsbiterrorrate ipv4framecount ipv6framecount ipv6overipv4framecount tcpframecount udpframecount mplsframecount icmpframecount vlanframecount ipv4framerate ipv6framerate ipv6overipv4framerate tcpframerate udpframerate mplsframerate icmpframerate vlanframerate trigger1count trigger1rate trigger2count trigger2rate trigger3count trigger3rate trigger4count trigger4rate trigger5count trigger5rate trigger6count trigger6rate trigger7count trigger7rate trigger8count trigger8rate combotriggercount combotriggerrate totalbitrate prbsbiterrorratio vlanframerate l1bitcount l1bitrate pfcframecount fcoeframecount pfcframerate fcoeframerate pfcpri0framecount pfcpri1framecount pfcpri2framecount pfcpri3framecount pfcpri4framecount pfcpri5framecount pfcpri6framecount pfcpri7framecount pfcpri0quanta pfcpri1quanta pfcpri2quanta pfcpri3quanta pfcpri4quanta pfcpri5quanta pfcpri6quanta pfcpri7quanta prbserrorframecount prbserrorframerate userdefinedframecount1 userdefinedframerate1 userdefinedframecount2 userdefinedframerate2 userdefinedframecount3 userdefinedframerate3 userdefinedframecount4 userdefinedframerate4 userdefinedframecount5 userdefinedframerate5 userdefinedframecount6 userdefinedframerate6 " \
        -interval 1 -filenamePrefix "stc_100mb_p1_rand_100L-0002-analyzerportresults"

    # Subscribe to results for result query stc_100mb_p1_rand_100L-0003-rxstreamsummaryresults
    stc::subscribe -parent [lindex [stc::get system1 -children-Project] 0] \
        -resultParent " [lindex [stc::get system1 -children-Project] 0] " \
        -configType streamblock \
        -resultType rxstreamsummaryresults \
        -filterList "[lindex [stc::get system1.Project(1) -children-RxPortResultFilter] 0] " \
        -viewAttributeList "framecount sigframecount fcserrorframecount minlatency maxlatency droppedframecount droppedframepercent inorderframecount reorderedframecount duplicateframecount lateframecount prbsbiterrorcount prbsfilloctetcount ipv4checksumerrorcount tcpudpchecksumerrorcount framerate sigframerate fcserrorframerate droppedframerate droppedframepercentrate inorderframerate reorderedframerate duplicateframerate lateframerate prbsbiterrorrate prbsfilloctetrate ipv4checksumerrorrate tcpudpchecksumerrorrate bitrate shorttermavglatency avglatency prbsbiterrorratio l1bitcount l1bitrate prbserrorframecount prbserrorframerate portstrayframes bitcount shorttermavgjitter avgjitter rfc4689absoluteavgjitter minjitter maxjitter shorttermavginterarrivaltime avginterarrivaltime mininterarrivaltime maxinterarrivaltime inseqframecount outseqframecount inseqframerate outseqframerate histbin1count histbin2count histbin3count histbin4count histbin5count histbin6count histbin7count histbin8count histbin9count histbin10count histbin11count histbin12count histbin13count histbin14count histbin15count histbin16count " \
        -interval 1 -filenamePrefix "stc_100mb_p1_rand_100L-0003-rxstreamsummaryresults"

    # Subscribe to results for result query stc_100mb_p1_rand_100L-0004-txstreamresults
    stc::subscribe -parent [lindex [stc::get system1 -children-Project] 0] \
        -resultParent " [lindex [stc::get system1 -children-Project] 0] " \
        -configType streamblock \
        -resultType txstreamresults \
        -filterList "" \
        -viewAttributeList "framecount framerate bitrate expectedrxframecount l1bitcount l1bitrate bitcount " \
        -interval 1 -filenamePrefix "stc_100mb_p1_rand_100L-0004-txstreamresults"

    # Start the sequencer
    stc::perform sequencerStart

    # Wait for sequencer to finish
    stc::waituntilcomplete

    # check the sequencer status and test state
    set sqrHandle [stc::get System1 -Children-Sequencer]
    set sqrStatus [stc::get $sqrHandle -Status]
    set sqrTestState [stc::get $sqrHandle -TestState]
    if { $sqrStatus eq "" }  {
        return $sqrTestState
    } else {
        return $sqrStatus
    }

}

#    cleanup - release the ports, disconnect from the chassis' and reset 
#              the in-memory configuration.
proc cleanup {} {
    stc::perform chassisDisconnectAll 
    stc::perform resetConfig -config system1
}