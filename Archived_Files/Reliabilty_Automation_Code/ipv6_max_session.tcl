package require SpirentTestCenter
source [ file join [ file dirname [ info script ] ] {ipv6_max_session_header.tcl} ]
puts "SpirentTestCenter system version:\t[stc::get system1 -Version]"
stc::config system1 -IsLoadingFromConfiguration "true"

#set value
set x 0
set start_capture 0
set Traffic_Hit 0
set Traffic_Hit_LOG "Traffic_Hit_LOG" 
set port1Mac 00:10:94:00:00:11
set port2Mac 00:10:95:00:00:11
set recordsperpage_limit 256

#PORT 1 StreamBlock Configuration
set port1Udpsrc1 1024
set port2Udpsrc1 1025

set stream_1_fram_config "<frame ><config><pdus><pdu name=\"ipv6\" pdu=\"ipv6:IPv6\"><trafficClass>0</trafficClass><flowLabel>7</flowLabel><payloadLength>8</payloadLength><hopLimit>255</hopLimit><sourceAddr>$port1Ipv6</sourceAddr><destAddr>$port2Ipv6</destAddr><prefixLength>64</prefixLength><destPrefixLength>64</destPrefixLength><gateway>$port1GatewayIpv6</gateway></pdu><pdu name=\"proto1\" pdu=\"udp:Udp\"><sourcePort>$port1Udpsrc1</sourcePort><destPort override=\"true\" >$port1Udpsrc1</destPort></pdu></pdus></config></frame>"

set stream_2_fram_config "<frame ><config><pdus><pdu name=\"ipv6\" pdu=\"ipv6:IPv6\"><trafficClass>0</trafficClass><flowLabel>7</flowLabel><payloadLength>8</payloadLength><hopLimit>255</hopLimit><sourceAddr>$port2Ipv6</sourceAddr><destAddr>$port1Ipv6</destAddr><prefixLength>64</prefixLength><destPrefixLength>64</destPrefixLength><gateway>$port2GatewayIpv6</gateway></pdu><pdu name=\"proto1\" pdu=\"udp:Udp\"><sourcePort>$port2Udpsrc1</sourcePort><destPort override=\"true\" >$port2Udpsrc1</destPort></pdu></pdus></config></frame>"


set project1 [stc::create "project" \
        -TableViewData "" \
        -SelectedTechnologyProfiles {} \
        -ConfigurationFileName {ipv6_max_session.tcl} ]


#create 2 port2
set port1 [stc::create port -under project1 -location $chassisIp/$por1Location]
set port2 [stc::create port -under project1 -location $chassisIp/$por2Location]

#connect to chassis and reserve port
stc::connect $chassisIp
stc::reserve $chassisIp/$por1Location
stc::reserve $chassisIp/$por2Location
stc::perform setupportmappings

#create device under ports
set EmulatedDevice1 [stc::create "EmulatedDevice" -under project1 -EnablePingResponse "TRUE" ]

set EthIIIf1 [stc::create "EthIIIf"  -under $EmulatedDevice1  -SourceMac $port1Mac -SrcMacList "" ]

set Ipv6If1 [stc::create "Ipv6If" \
        -under $EmulatedDevice1 \
        -Address $port1Ipv6\
        -AddrList "" \
        -Gateway $port1GatewayIpv6 \
        -GatewayList "" \
        -ResolveGatewayMac "TRUE" \
        -GatewayMac $port1GatewayMac ]

set EmulatedDevice2 [stc::create "EmulatedDevice" -under project1 -DeviceCount $session_count -EnablePingResponse "TRUE" ]

set EthIIIf2 [stc::create "EthIIIf"  -under $EmulatedDevice2  -SourceMac $port2Mac -SrcMacList "" ]

set Ipv6If2 [stc::create "Ipv6If" \
        -under $EmulatedDevice2 \
        -Address $port2Ipv6 \
        -AddrList "" \
        -Gateway $port2GatewayIpv6 \
        -GatewayList "" \
        -ResolveGatewayMac "TRUE" \
        -GatewayMac $port2GatewayMac ]

stc::config $EmulatedDevice1 -AffiliationPort-targets $port1
stc::config $EmulatedDevice1 -TopLevelIf-targets $Ipv6If1
stc::config $EmulatedDevice1 -PrimaryIf-targets $Ipv6If1
stc::config $Ipv6If1 -StackedOnEndpoint-targets $EthIIIf1

stc::config $EmulatedDevice2 -AffiliationPort-targets $port2
stc::config $EmulatedDevice2 -TopLevelIf-targets $Ipv6If2
stc::config $EmulatedDevice2 -PrimaryIf-targets $Ipv6If2
stc::config $Ipv6If2 -StackedOnEndpoint-targets $EthIIIf2


#create 8 streamblock on port1
puts "Configuring StreamBlock (1)"
set streamblock1 [stc::create streamblock -under $port1 \
        -FixedFrameLength $frameLengh \
	-InsertSig "TRUE" \
        -FrameConfig $stream_1_fram_config ]
stc::config $streamblock1 -SrcBinding-targets $Ipv6If1
stc::config $streamblock1 -DstBinding-targets $Ipv6If2
set streamBlockLoadProfile1 [stc::create "streamBlockLoadProfile" -under project1 -Load $up_stream_load -LoadUnit "MEGABITS_PER_SECOND" ]
stc::config $streamblock1 -AffiliationStreamBlockLoadProfile-targets $streamBlockLoadProfile1

puts "Configuring StreamBlock (2)"
set streamblock2 [stc::create streamblock -under $port2 \
        -FixedFrameLength $frameLengh \
	-InsertSig "TRUE" \
        -FrameConfig $stream_2_fram_config ]
stc::config $streamblock2 -SrcBinding-targets $Ipv6If2
stc::config $streamblock2 -DstBinding-targets $Ipv6If1
set streamBlockLoadProfile2 [stc::create "streamBlockLoadProfile" -under project1 -Load $down_stream_load -LoadUnit "MEGABITS_PER_SECOND" ] 
stc::config $streamblock2 -AffiliationStreamBlockLoadProfile-targets $streamBlockLoadProfile2

#Config generator
set generator1 [lindex [stc::get $port1 -children-generator] 0]
set generatorconfig1 [lindex [stc::get $generator1 -children-generatorConfig] 0]
stc::config $generatorconfig1 \
        -SchedulingMode "RATE_BASED" \
        -Duration $runTime \
        -DurationMode "SECONDS"

set generator2 [lindex [stc::get $port2 -children-generator] 0]
set generatorconfig2 [lindex [stc::get $generator2 -children-generatorConfig] 0]
stc::config $generatorconfig2 \
        -SchedulingMode "RATE_BASED" \
        -Duration $runTime \
        -DurationMode "SECONDS"

if { $up_stream_result_capture } {
	set port "port1"
	set load_unit $up_stream_load
	puts "UP STREAM CAPTURE via $port with Load set to $load_unit MB"
} elseif { $down_stream_result_capture } {
	set port "port2"
	set load_unit $down_stream_load
	puts "DOWN STREAM CAPTURE via $port with Load set to $load_unit MB"
} else {
	puts "UP or DOWN STREAM CAPTURE PORT NOT ENABLED "
	stc::connect $chassisIp
	stc::release $chassisIp/$por1Location
	stc::release $chassisIp/$por2Location
	stc::disconnect $chassisIp
}

set Megabytes [expr {1000 * 1000 * $load_unit}]
set expected_l1bitrate_per_stream [expr {$Megabytes / $session_count}]
set min_range [expr {(1 - ($resolution/2)) * $expected_l1bitrate_per_stream }]
set max_range [expr {(1 + ($resolution/2)) * $expected_l1bitrate_per_stream }]

puts Megabytes=$Megabytes
puts expected_l1bitrate_per_stream=$expected_l1bitrate_per_stream
puts min_range=$min_range
puts max_range=$max_range

#start traffic 
stc::apply

# Subscribe to results for result query Port-filteredstreamresults
set hResultDataSet [stc::subscribe -parent [lindex [stc::get system1 -children-Project] 0] \
        -resultParent $port  \
        -configType streamblock \
	-recordsperpage $recordsperpage_limit \
        -resultType rxstreamsummaryresults \
        -filterList "[lindex [stc::get system1.Project(1) -children-RxPortResultFilter] 0] " \
        -viewAttributeList "framecount bitcount l1bitrate l1bitcount Comp32 " \
        -interval 1 -filenamePrefix "ipv6_max_session-0001-rxstreamsummaryresults"]

stc::subscribe -parent [lindex [stc::get system1 -children-Project] 0] \
        -resultParent " [lindex [stc::get system1 -children-Project] 0] " \
        -configType streamblock \
	-recordsperpage $recordsperpage_limit \
        -resultType txstreamresults \
        -filterList "" \
        -viewAttributeList "framecount framerate bitrate expectedrxframecount l1bitcount l1bitrate bitcount " \
        -interval 1 -filenamePrefix "ipv6_max_session-0001-txstreamresults"

stc::perform generatorstart -generatorlist "$generator1 $generator2"
set streamcount 1
while {$x < $runTime} {
	foreach hResults [stc::get $hResultDataSet -ResultHandleList] {
		array set aResults [stc::get $hResults]       
		set isMatch_start [string match "rxstreamsummaryresults$streamcount" $hResults]
		set isMatch_end [string match "rxstreamsummaryresults$session_count" $hResults]
		if { $isMatch_start != 0 && $aResults(-L1BitRate) != 0 && $start_capture == 0} {
			set start_capture 1
		}

		if { $start_capture == 1 && $aResults(-L1BitRate) >= $min_range && $aResults(-L1BitRate) <= $max_range } {
				incr Traffic_Hit
		                set streamcount [expr {$streamcount + 1}]
				puts "$hResults\tStream Id: $aResults(-Comp32)\tFrameCount $aResults(-FrameCount)\tL1BitRate: $aResults(-L1BitRate)"
		} elseif { $start_capture == 1 && $aResults(-L1BitRate) == 0 } {
#				puts "NO_TRAFFIC:$hResults\tStream Id: $aResults(-Comp32)\tFrameCount $aResults(-FrameCount)\tL1BitRate: $aResults(-L1BitRate)"
				set start_capture 0
		}

		if { $isMatch_end != 0 && $start_capture == 1} {
			puts "TRAFFIC HIT NO : $Traffic_Hit"
			stc::connect $chassisIp
			stc::release $chassisIp/$por1Location
			stc::release $chassisIp/$por2Location
			stc::disconnect $chassisIp
			set fileId [open $Traffic_Hit_LOG "w"]
		        puts -nonewline $fileId $Traffic_Hit
		        close $fileId
			exit 0
		}
	 }
	set x [expr {$x + 1}]
	after 1000

}

stc::perform GeneratorWaitForStopCommand -generatorlist "$generator1 $generator2"

#Finish script
stc::connect $chassisIp
stc::release $chassisIp/$por1Location
stc::release $chassisIp/$por2Location
stc::disconnect $chassisIp

