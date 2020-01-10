Name:    kdeplasma-addons
Summary: Additional plasmoids for KDE
Version: 4.10.5
Release: 3%{?dist}

License: GPLv2+
URL:     http://www.kde.org/
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/%{version}/src/%{name}-%{version}.tar.xz

# upstreamable patches

# upstream patches

# rhel patches
Patch300: kdeplasma-addons-4.10.3-rhel.patch

BuildRequires: boost-devel
BuildRequires: gettext
BuildRequires: kdepimlibs-devel >= %{version}
# for libplasmaclock
BuildRequires: kde-workspace-devel >= %{version}
%if 0%{?fedora}
BuildRequires: pkgconfig(eigen2)
BuildRequires: pkgconfig(libqalculate)
# plasma-wallpaper-marble 
BuildRequires: marble-devel >= 1:%{version}
# Plasma Microblog DataEngine
BuildRequires: pkgconfig(qoauth)
# plasma-applet-kimpanel
BuildRequires: pkgconfig(ibus-1.0)
# FIXME: be mindful of this if building locally -- rex
BuildConflicts: pkgconfig(qwt5-qt4)
BuildRequires: pkgconfig(qwt)
%endif
BuildRequires: pkgconfig(dbusmenu-qt)
BuildRequires: pkgconfig(libattica)
BuildRequires: pkgconfig(libkexiv2) >= 0.4.0
BuildRequires: pkgconfig(qca2)
BuildRequires: pkgconfig(qimageblitz)
BuildRequires: pkgconfig(QJson)
# lancelot eye-candy
BuildRequires: pkgconfig(xcomposite) pkgconfig(xdamage) pkgconfig(xrender)

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

# included in since 4.6 (f15)
Obsoletes: plasma-runner-events < 0.3.0-100
Provides:  plasma-runner-events = 0.3.0-100

%{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }

# dataengines
Provides: plasma-dataengine-comic = %{version}-%{release}
Provides: plasma-dataengine-microblog = %{version}-%{release}
Provides: plasma-dataengine-ocs = %{version}-%{release}
Provides: plasma-dataengine-potd = %{version}-%{release}

Obsoletes: plasma-icontasks < 1.0
Provides:  plasma-icontasks = 1.0

%description
Additional plasmoids for KDE.

%package libs
Summary: Runtime libraries for %{name}
Requires: %{name} = %{version}-%{release}
Requires: kdelibs4%{?_isa} >= %{version}
%description libs
%{summary}.

%package devel
Summary:  Developer files for %{name}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kdelibs4-devel
Requires: plasma-devel
%description devel
Files for developing applications using %{name}.

%package -n plasma-applet-kimpanel
Summary: Plasma applet for input methods
%description -n plasma-applet-kimpanel
%{summary}, including ibus.

%package -n plasma-wallpaper-marble
Summary:  Marble wallpaper for kde-plasma 
Requires: marble%{?_kde4_version: >= 1:%{_kde4_version}}
%description -n plasma-wallpaper-marble 
%{summary}.


%prep
%setup -q -n kdeplasma-addons-%{version}%{?alphatag}

%if 0%{?rhel}
%patch300 -p1 -b .rhel
%endif

# rename some icons that conflict with kamoso
pushd runners/youtube
sed -i.bak -e 's|^Icon=youtube|Icon=krunner_youtube|' *.desktop
for icon in icons/*-action-youtube.* ; do
  new_name=$(echo ${icon} | sed -e's|-youtube|-krunner_youtube|')
  mv ${icon} ${new_name}
done
popd


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

## unpackaged files
rm -f %{buildroot}%{_kde4_libdir}/lib{plasma*,rtm}.so


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
fi

%files
%doc COPYING COPYING.LIB
%{_kde4_bindir}/lancelot
%{_kde4_appsdir}/bball/
# lancelot theme goodies
%{_kde4_appsdir}/desktoptheme/*
%{_kde4_appsdir}/lancelot/
%{_kde4_appsdir}/plasmaboard/
%{_kde4_appsdir}/plasma/packages/org.kde.comic/
%{_kde4_appsdir}/plasma/packages/org.kde.lcdweather/
%{_kde4_appsdir}/plasma/packages/org.kde.weather/
%{_kde4_appsdir}/plasma/plasmoids/calculator/
%{_kde4_appsdir}/plasma/plasmoids/nowplaying/
%{_kde4_appsdir}/plasma/plasmoids/konqprofiles/
%{_kde4_appsdir}/plasma/plasmoids/konsoleprofiles/
%{_kde4_appsdir}/plasma/wallpapers/org.kde.animals/
%{_kde4_appsdir}/plasma/wallpapers/org.kde.haenau/
%{_kde4_appsdir}/plasma/wallpapers/org.kde.hunyango/
%{_kde4_appsdir}/plasma/services/org.kde.plasma.dataengine.konqprofiles.operations
%{_kde4_appsdir}/plasma/services/org.kde.plasma.dataengine.konsoleprofiles.operations
%{_kde4_appsdir}/plasma-applet-frame/
%if 0%{?fedora}
%{_kde4_appsdir}/plasma-applet-opendesktop/
%endif
%{_kde4_appsdir}/plasma-applet-opendesktop-activities/
%{_kde4_appsdir}/plasma_pastebin/
%{_kde4_appsdir}/plasma_wallpaper_pattern/
%{_kde4_appsdir}/rssnow/
%{_kde4_libdir}/kde4/kcm_krunner_dictionary.so
%{_kde4_libdir}/kde4/kcm_krunner_audioplayercontrol.so
%{_kde4_libdir}/kde4/kcm_krunner_charrunner.so
%{_kde4_libdir}/kde4/kcm_krunner_spellcheck.so
%{_kde4_libdir}/kde4/kcm_plasma_runner_events.so
%{_kde4_libdir}/kde4/krunner_audioplayercontrol.so
%{_kde4_libdir}/kde4/krunner_browserhistory.so
%{_kde4_libdir}/kde4/krunner_charrunner.so
%{_kde4_libdir}/kde4/krunner_contacts.so
%{_kde4_libdir}/kde4/krunner_converter.so
%{_kde4_libdir}/kde4/krunner_dictionary.so
%{_kde4_libdir}/kde4/krunner_katesessions.so
%{_kde4_libdir}/kde4/krunner_konquerorsessions.so
%{_kde4_libdir}/kde4/krunner_konsolesessions.so
%{_kde4_libdir}/kde4/krunner_kopete.so
%{_kde4_libdir}/kde4/krunner_mediawiki.so
%{_kde4_libdir}/kde4/krunner_spellcheckrunner.so
%{_kde4_libdir}/kde4/krunner_youtube.so
%{_kde4_libdir}/kde4/plasma-applet_systemloadviewer.so
%{_kde4_libdir}/kde4/plasma_applet_bball.so
%{_kde4_libdir}/kde4/plasma_applet_binaryclock.so
%{_kde4_libdir}/kde4/plasma_applet_blackboard.so
%{_kde4_libdir}/kde4/plasma_applet_bookmarks.so
%{_kde4_libdir}/kde4/plasma_applet_bubblemon.so
%{_kde4_libdir}/kde4/plasma_applet_charselect.so
%{_kde4_libdir}/kde4/plasma_applet_comic.so
%{_kde4_libdir}/kde4/plasma_applet_eyes.so
%{_kde4_libdir}/kde4/plasma_applet_fifteenPuzzle.so
%{_kde4_libdir}/kde4/plasma_applet_fileWatcher.so
%{_kde4_libdir}/kde4/plasma_applet_frame.so
%{_kde4_libdir}/kde4/plasma_applet_fuzzy_clock.so
%{_kde4_libdir}/kde4/plasma_applet_icontasks.so
%{_kde4_libdir}/kde4/plasma_applet_incomingmsg.so
%if 0%{?fedora}
%{_kde4_libdir}/kde4/plasma_applet_kdeobservatory.so
%endif
%{_kde4_libdir}/kde4/plasma_applet_knowledgebase.so
%{_kde4_libdir}/kde4/plasma_applet_kolourpicker.so
%{_kde4_libdir}/kde4/plasma_applet_lancelot_launcher.so
%{_kde4_libdir}/kde4/plasma_applet_lancelot_part.so
%{_kde4_libdir}/kde4/plasma_applet_leavenote.so
%{_kde4_libdir}/kde4/plasma_applet_life.so
%{_kde4_libdir}/kde4/plasma_applet_luna.so
%{_kde4_libdir}/kde4/plasma_applet_magnifique.so
%{_kde4_libdir}/kde4/plasma_applet_mediaplayer.so
%{_kde4_libdir}/kde4/plasma_applet_microblog.so
%{_kde4_libdir}/kde4/plasma_applet_notes.so
%if 0%{?fedora}
%{_kde4_libdir}/kde4/plasma_applet_dict.so
%{_kde4_libdir}/kde4/plasma_applet_opendesktop.so
%{_kde4_libdir}/kde4/plasma_applet_news.so
%{_kde4_libdir}/kde4/plasma_applet_qalculate.so
%{_kde4_libdir}/kde4/plasma_applet_rtm.so
%{_kde4_libdir}/kde4/plasma_applet_webslice.so
%{_kde4_libdir}/kde4/plasma_engine_rtm.so
%{_kde4_libdir}/kde4/plasma_wallpaper_mandelbrot.so
%{_kde4_libdir}/kde4/plasma_engine_microblog.so
%endif
%{_kde4_libdir}/kde4/plasma_wallpaper_qml.so
%{_kde4_libdir}/kde4/plasma_applet_opendesktop_activities.so
%{_kde4_libdir}/kde4/plasma_applet_paste.so
%{_kde4_libdir}/kde4/plasma_applet_pastebin.so
%{_kde4_libdir}/kde4/plasma_applet_plasmaboard.so
%{_kde4_libdir}/kde4/plasma_applet_previewer.so
%{_kde4_libdir}/kde4/plasma_applet_rssnow.so
%{_kde4_libdir}/kde4/plasma_applet_showdashboard.so
%{_kde4_libdir}/kde4/plasma_applet_showdesktop.so
%{_kde4_libdir}/kde4/plasma_applet_spellcheck.so
%{_kde4_libdir}/kde4/plasma_applet_timer.so
%{_kde4_libdir}/kde4/plasma_applet_unitconverter.so
%{_kde4_libdir}/kde4/plasma_applet_weather.so
%{_kde4_libdir}/kde4/plasma_applet_weatherstation.so
%{_kde4_libdir}/kde4/plasma_comic_krossprovider.so
%{_kde4_libdir}/kde4/plasma_containment_griddesktop.so
%{_kde4_libdir}/kde4/plasma_containment_groupingdesktop.so
%{_kde4_libdir}/kde4/plasma_containment_groupingpanel.so
%{_kde4_libdir}/kde4/plasma_engine_comic.so
%{_kde4_libdir}/kde4/plasma_engine_kdeobservatory.so
%{_kde4_libdir}/kde4/plasma_engine_konqprofiles.so
%{_kde4_libdir}/kde4/plasma_engine_konsoleprofiles.so
%{_kde4_libdir}/kde4/plasma_engine_ocs.so
%{_kde4_libdir}/kde4/plasma_engine_potd.so
%{_kde4_libdir}/kde4/plasma_packagestructure_comic.so
%{_kde4_libdir}/kde4/plasma_potd_apodprovider.so
%{_kde4_libdir}/kde4/plasma_potd_epodprovider.so
%{_kde4_libdir}/kde4/plasma_potd_flickrprovider.so
%{_kde4_libdir}/kde4/plasma_potd_oseiprovider.so
%{_kde4_libdir}/kde4/plasma_potd_wcpotdprovider.so
%{_kde4_libdir}/kde4/plasma_runner_datetime.so
%{_kde4_libdir}/kde4/plasma_runner_events.so
%{_kde4_libdir}/kde4/plasma_wallpaper_pattern.so
%{_kde4_libdir}/kde4/plasma_wallpaper_potd.so
%{_kde4_libdir}/kde4/plasma_wallpaper_virus.so
%{_kde4_libdir}/kde4/plasma_wallpaper_weather.so
%{_kde4_configdir}/comic.knsrc
%{_kde4_configdir}/pastebin.knsrc
%{_kde4_configdir}/plasmaweather.knsrc
%{_kde4_configdir}/virus_wallpaper.knsrc
%{_kde4_appsdir}/kdeplasma-addons/mediabuttonsrc
%{_kde4_appsdir}/plasma/services/kdeobservatory.operations
%{_kde4_appsdir}/plasma/services/ocsPerson.operations
%if 0%{?fedora}
%{_kde4_appsdir}/plasma/services/rtmauth.operations
%{_kde4_appsdir}/plasma/services/rtmtask.operations
%{_kde4_appsdir}/plasma/services/rtmtasks.operations
%{_kde4_appsdir}/plasma/services/tweet.operations
%endif
%{_kde4_datadir}/kde4/services/CharRunner_config.desktop
%{_kde4_datadir}/kde4/services/CharacterRunner.desktop
%{_kde4_datadir}/kde4/services/ServiceMenus/preview.desktop
%{_kde4_datadir}/kde4/services/apodprovider.desktop
%{_kde4_datadir}/kde4/services/browserhistory.desktop
%{_kde4_datadir}/kde4/services/epodprovider.desktop
%{_kde4_datadir}/kde4/services/flickrprovider.desktop
%{_kde4_datadir}/kde4/services/katesessions.desktop
%{_kde4_datadir}/kde4/services/konquerorsessions.desktop
%{_kde4_datadir}/kde4/services/konsolesessions.desktop
%{_kde4_datadir}/kde4/services/lancelot.desktop
%{_kde4_datadir}/kde4/services/oseiprovider.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-bball.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-binaryclock.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-blackboard.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-bookmarks.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-bubblemon.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-calculator.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-charselect.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-eyes.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-fifteenPuzzle.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-icontasks.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-incomingmsg.desktop
%if 0%{?fedora}
%{_kde4_datadir}/kde4/services/plasma-applet-kdeobservatory.desktop
%endif
%{_kde4_datadir}/kde4/services/plasma-applet-knowledgebase.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-konqprofiles.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-konsoleprofiles.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-lancelot-launcher.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-lancelot-part.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-leavenote.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-life.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-luna.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-magnifique.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-mediaplayer.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-microblog.desktop
%if 0%{?fedora}
%{_kde4_datadir}/kde4/services/plasma-applet-news.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-opendesktop.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-qalculate.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-rememberthemilk.desktop
%{_kde4_datadir}/kde4/services/plasma-dict-default.desktop
%{_kde4_datadir}/kde4/services/plasma-engine-rtm.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-webslice.desktop
%{_kde4_datadir}/kde4/services/plasma-wallpaper-mandelbrot.desktop
%{_kde4_datadir}/kde4/services/plasma-dataengine-microblog.desktop
%endif
%{_kde4_datadir}/kde4/services/plasma-applet-nowplaying.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-opendesktop-activities.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-paste.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-pastebin.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-previewer.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-rssnow.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-showdashboard.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-showdesktop.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-spellcheck.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-systemloadviewer.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-timer.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-unitconverter.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-weather.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-weatherstation.desktop
%{_kde4_datadir}/kde4/services/plasma-clock-fuzzy.desktop
%{_kde4_datadir}/kde4/services/plasma-comic-default.desktop
%{_kde4_datadir}/kde4/services/plasma-containment-griddesktop.desktop
%{_kde4_datadir}/kde4/services/plasma-containment-groupingdesktop.desktop
%{_kde4_datadir}/kde4/services/plasma-containment-groupingpanel.desktop
%{_kde4_datadir}/kde4/services/plasma-dataengine-comic.desktop
%{_kde4_datadir}/kde4/services/plasma-dataengine-konqprofiles.desktop
%{_kde4_datadir}/kde4/services/plasma-dataengine-konsoleprofiles.desktop
%{_kde4_datadir}/kde4/services/plasma-dataengine-ocs.desktop
%{_kde4_datadir}/kde4/services/plasma-dataengine-potd.desktop
%{_kde4_datadir}/kde4/services/plasma-engine-kdeobservatory.desktop
%{_kde4_datadir}/kde4/services/plasma-fileWatcher-default.desktop
%{_kde4_datadir}/kde4/services/plasma-frame-default.desktop
%{_kde4_datadir}/kde4/services/plasma-kolourpicker-default.desktop
%{_kde4_datadir}/kde4/services/plasma-notes-default.desktop
%{_kde4_datadir}/kde4/services/plasma-packagestructure-comic.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-audioplayercontrol.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-audioplayercontrol_config.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-contacts.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-converter.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-datetime.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-dictionary.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-dictionary_config.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-events.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-events_config.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-kopete.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-spellchecker.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-spellchecker_config.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-techbase.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-wikipedia.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-wikitravel.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-youtube.desktop
%{_kde4_datadir}/kde4/services/plasma-wallpaper-pattern.desktop
%{_kde4_datadir}/kde4/services/plasma-wallpaper-potd.desktop
%{_kde4_datadir}/kde4/services/plasma-wallpaper-qml.desktop
%{_kde4_datadir}/kde4/services/plasma-wallpaper-virus.desktop
%{_kde4_datadir}/kde4/services/plasma-wallpaper-weather.desktop
%{_kde4_datadir}/kde4/services/plasma_applet_plasmaboard.desktop
%{_kde4_datadir}/kde4/services/wcpotdprovider.desktop
%{_kde4_datadir}/kde4/servicetypes/plasma_comicprovider.desktop
%{_kde4_datadir}/kde4/servicetypes/plasma_potdprovider.desktop
%{_kde4_datadir}/mime/packages/lancelotpart-mime.xml
%{_kde4_iconsdir}/hicolor/*/actions/*youtube.*
%{_kde4_iconsdir}/hicolor/*/apps/*

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kde4_libdir}/liblancelot.so.*
%{_kde4_libdir}/liblancelot-datamodels.so.*
%{_kde4_libdir}/libplasmapotdprovidercore.so.*
%{_kde4_libdir}/libplasmacomicprovidercore.so.*
%{_kde4_libdir}/libplasma_groupingcontainment.so.*
%{_kde4_libdir}/libplasmaweather.so.*
%if 0%{?fedora}
%{_kde4_libdir}/librtm.so.*
%endif

%files devel
%{_kde4_appsdir}/cmake/modules/FindLancelot-Datamodels.cmake
%{_kde4_appsdir}/cmake/modules/FindLancelot.cmake
%{_kde4_includedir}/lancelot/
%{_kde4_includedir}/lancelot-datamodels/
%{_kde4_includedir}/KDE/Lancelot/
%{_kde4_libdir}/liblancelot.so
%{_kde4_libdir}/liblancelot-datamodels.so

%if 0%{?fedora}
%files -n plasma-applet-kimpanel
%doc applets/kimpanel/COPYING
%{_kde4_libdir}/kde4/plasma_engine_kimpanel.so
%{_kde4_libdir}/kde4/plasma_applet_kimpanel.so
%{_kde4_libexecdir}/kimpanel-ibus-panel
%{_kde4_appsdir}/plasma/services/kimpanel.operations
%{_kde4_datadir}/kde4/services/plasma-applet-kimpanel.desktop
%{_kde4_datadir}/kde4/services/plasma-dataengine-kimpanel.desktop
%{_kde4_datadir}/config.kcfg/kimpanelconfig.kcfg

%files -n plasma-wallpaper-marble
%doc COPYING
%{_kde4_libdir}/kde4/plasma_wallpaper_marble.so
%{_kde4_datadir}/kde4/services/plasma-wallpaper-marble.desktop
%endif


%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 4.10.5-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 4.10.5-2
- Mass rebuild 2013-12-27

* Sun Jun 30 2013 Than Ngo <than@redhat.com> - 4.10.5-1
- 4.10.5

* Mon Jun 03 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.4-2
- spec cleanup
- Weak passwords generated by PasteMacroExpander (#969421,#969425)

* Sat Jun 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.4-1
- 4.10.4

* Wed May 22 2013 Lukáš Tinkl <ltinkl@redhat.com> - 4.10.3-2
- require libqalculate under Fedora only

* Mon May 06 2013 Than Ngo <than@redhat.com> - 4.10.3-1
- 4.10.3

* Mon Apr 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- 4.10.2

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-1
- 4.10.1

* Fri Feb 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.0-1
- 4.10.0

* Sun Jan 20 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.98-1
- 4.9.98

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.97-1
- 4.9.97

* Fri Dec 21 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.95-2
- drop explicit BR: nepomuk-core-devel hack (kdepimlibs fixed)

* Thu Dec 20 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.95-1
- 4.9.95

* Tue Dec 04 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.90-2
- rebuild (kde-settings' plasma4.req fixes)

* Tue Dec 04 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.90-1
- 4.9.90

* Mon Dec 03 2012 Than Ngo <than@redhat.com> - 4.9.4-1
- 4.9.4

* Thu Nov 29 2012 Dan Vrátil <dvratil@redhat.com> - 4.9.3-6
- Store position of widgets in vertical Grouping Panel (#879802)

* Tue Nov 27 2012 Dan Vrátil <dvratil@redhat.com> - 4.9.3-5
- Rebuild against qjson 0.8.1

* Fri Nov 23 2012 Dan Vratil <dvratil@redhat.com> - 4.9.3-4
- Rebuild against qjson 0.8.0

* Fri Nov 16 2012 Than Ngo <than@redhat.com> - 4.9.3-3
- clean up

* Mon Nov 12 2012 Lukáš Tinkl <ltinkl@redhat.com> - 4.9.3-2
- libqwt-devel only on Fedora

* Sat Nov 03 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.3-1
- 4.9.3

* Sat Sep 29 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- 4.9.2

* Mon Sep 03 2012 Than Ngo <than@redhat.com> - 4.9.1-1
- 4.9.1

* Mon Aug 06 2012 Than Ngo <than@redhat.com> - 4.9.0-2
- add fedora/rhel condition

* Thu Jul 26 2012 Lukas Tinkl <ltinkl@redhat.com> - 4.9.0-1
- 4.9.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.97-1
- 4.8.97

* Wed Jun 27 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.95-1
- 4.8.95

* Wed Jun 20 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.90-3
- rebuild (attica)

* Mon Jun 11 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.90-2
- rename youtube krunner icons to avoid conflict with kamoso

* Sun Jun 10 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.90-1
- 4.8.90

* Sun Jun 03 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.80-1
- 4.8.80

* Tue May 08 2012 Than Ngo <than@redhat.com> - 4.8.3-2
- add rhel/fedora condition

* Mon Apr 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.3-1
- 4.8.3

* Fri Mar 30 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-1
- 4.8.2

* Mon Mar 19 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.8.1-3
- rebuild for plasma4.prov fix (no more spaces in Plasma runner auto-Provides)

* Sat Mar 10 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.8.1-2
- reenable kimpanel ibus backend
- fix kimpanel ibus backend build with ibus 1.4.99

* Mon Mar 05 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.1-1
- 4.8.1

* Sun Jan 22 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.0-1
- 4.8.0

* Wed Jan 04 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.7.97-1
- 4.7.97
- kimpanel: omit ibus backend on f17+ FTBFS (#771115)
- add patch that fix shadowning variable

* Sat Dec 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.95-3
- rebuild (attica)

* Sat Dec 24 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.95-2
- Obsoletes/Provides: plasma-icontasks

* Wed Dec 21 2011 Radek Novacek <rnovacek@redhat.com> - 4.7.95-1
- 4.7.95

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.90-1
- 4.7.90
- plasma-applet-kimpanel

* Fri Dec 02 2011 Than Ngo <than@redhat.com> - 4.7.80-2
- fix rhel/fedora condition

* Fri Nov 25 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.80-1
- 4.7.80

* Sat Oct 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-1
- 4.7.3

* Wed Oct 05 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1
- 4.7.2

* Wed Sep 28 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-2
- pkgconfig-style deps
- fix marble deps
- drop old/deprecated Obsoletes/Provides

* Fri Sep 02 2011 Than Ngo <than@redhat.com> - 4.7.1-1
- 4.7.1

* Sun Aug 21 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7.0-4
- rebuild again for the fixed RPM dependency generators for Plasma (#732271)

* Sun Aug 21 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7.0-3
- rebuild for the RPM dependency generators for Plasma (GSoC 2011)

* Mon Aug 08 2011 Radek Novacek <rnovacek@redhat.com> 4.7.0-2
- Fix crash with Group Desktop plasma option (fixed upstream)
- https://bugs.kde.org/show_bug.cgi?id=278222#c16

* Tue Jul 26 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.0-1
- 4.7.0

* Thu Jul 21 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.95-2
- rebuild (qt48)

* Mon Jul 11 2011 Jaroslav Reznik <jreznik@redhat.com> 4.6.95-1
- 4.6.95

* Fri Jul 01 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.90-2
- s/libkexiv2-devel/pkgconfig(libkexiv2)/

* Mon Jun 27 2011 Than Ngo <than@redhat.com> - 4.6.90-1
- 4.6.90 (rc1)

* Tue Jun 14 2011 Jaroslav Reznik <jreznik@redhat.com> - 4.6.80-1
- 4.6.80 (beta1)

* Fri May 06 2011 Than Ngo <than@redhat.com> - 4.6.3-1
- 4.6.3

* Wed Apr 06 2011 Than Ngo <than@redhat.com> - 4.6.2-1
- 4.6.2

* Mon Feb 28 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.1-1
- 4.6.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.0-2
- Obsoletes/Provides: plasma-runner-events
- drop old Obsoletes (f15+)

* Fri Jan 21 2011 Jaroslav Reznik <jreznik@redhat.com> 4.6.0-1
- 4.6.0

* Thu Jan 06 2011 Jaroslav Reznik <jreznik@redhat.com> 4.5.95-1
- 4.5.95 (4.6rc2)

* Wed Dec 22 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5.90-1
- 4.5.90 (4.6rc1)

* Sat Dec 04 2010 Thomas Janssen <thomasj@fedoraproject.org> 4.5.85-1
- 4.5.85 (4.6beta2)

* Mon Nov 22 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.80-2
- rebuild against fixed kdeedu-devel to pick up FindMarble.cmake

* Sun Nov 21 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.80-1
- 4.5.80 (4.6beta1)

* Sun Oct 31 2010 Than Ngo <than@redhat.com> - 4.5.3-1
- 4.5.3

* Sun Oct 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-2
- Spelling error in plasma-wallpaper-marble's Summary (#600634)

* Sat Oct 02 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-1
- 4.5.2

* Fri Aug 27 2010 Jaroslav Reznik <jreznik@redhat.com> - 4.5.1-1
- 4.5.1

* Tue Aug 03 2010 Than Ngo <than@redhat.com> - 4.5.0-1
- 4.5.0

* Sun Jul 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.95-1
- 4.5 RC3 (4.4.95)

* Wed Jul 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.92-1
- 4.5 RC2 (4.4.92)

* Fri Jun 25 2010 Jaroslav Reznik <jreznik@redhat.com> - 4.4.90-1
- 4.5 RC1 (4.4.90)

* Mon Jun 07 2010 Jaroslav Reznik <jreznik@redhat.com> - 4.4.85-1
- 4.5 Beta 2 (4.4.85)

* Fri May 21 2010 Jaroslav Reznik <jreznik@redhat.com> - 4.4.80-1
- 4.5 Beta 1 (4.4.80)

* Fri Apr 30 2010 Jaroslav Reznik <jreznik@redhat.com> - 4.4.3-1
- 4.4.3

* Mon Mar 29 2010 Lukas Tinkl <ltinkl@redhat.com> - 4.4.2-1
- 4.4.2

* Sat Feb 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.1-1
- 4.4.1

* Fri Feb 05 2010 Than Ngo <than@redhat.com> - 4.4.0-1
- 4.4.0

* Sun Jan 31 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.98-1
- KDE 4.3.98 (4.4rc3)

* Sun Jan 31 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.95-4
- plasma-wallpaper-marble subpkg (#556964)
- Provides: plasma-dataengine-{comic,microblog,ocs,potd}

* Sat Jan 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.95-3
- BR: qwt-devel (kdeobservatory)

* Fri Jan 29 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.95-2
- drop krunner_contacts_not_enabledbydefault.patch, handled 
  elsewhere (kde-settings/krunnerrc)

* Wed Jan 20 2010 Lukas Tinkl <ltinkl@redhat.com> - 4.3.95-1
- KDE 4.3.95 (4.4rc2)

* Sat Jan 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.90-2
- rebuild (boost)

* Wed Jan 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.90-1
- kde-4.3.90 (4.4rc1)

* Fri Dec 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.85-1
- kde-4.3.85 (4.4beta2)

* Tue Dec  1 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.3.80-1
- KDE 4.4 beta1 (4.3.80)

* Tue Nov 24 2009 Ben Boeckel <MathStuf@gmail.com> - 4.3.75-0.1.svn1048496
- Update to 4.3.75 snapshot

* Sat Oct 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Mon Oct 26 2009 Than Ngo <than@redhat.com> - 4.3.2-5
- remove duplicate BR on eigen2-devel

* Tue Oct 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.2-4
- rebuild (eigen2)

* Fri Oct 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.2-3
- rev microblog/twitter patch (kde#200475#c36)

* Sat Oct 10 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.2-2
- microblog/twitter fix (kde#209891)

* Mon Oct 05 2009 Than Ngo <than@redhat.com> - 4.3.2-1
- 4.3.2

* Sat Oct 03 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.1-3
- Ship -devel subpackage (#527011)

* Wed Sep 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-2
- Microblogging Widget Does Not Fetch Tweets (#526524)

* Fri Aug 28 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1

* Thu Aug 13 2009 Than Ngo <than@redhat.com> - 4.3.0-9
- omit BR on kdeedu-devel/eigen2-devel for rhel

* Fri Aug 07 2009 Ben Boeckel <MathStuf@gmail.com> - 4.3.0-8
- Waited for newRepo task

* Fri Aug 07 2009 Ben Boeckel <MathStuf@gmail.com> - 4.3.0-7
- Rebuild for mising rawhide oxygen-icon-theme
- Fix patch comments

* Fri Aug 07 2009 Ben Boeckel <MathStuf@gmail.com> - 4.3.0-6
- Add patch to fix kde#196809

* Tue Aug 04 2009 Than Ngo <than@redhat.com> - 4.3.0-5
- respin

* Mon Aug 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-4
- fix microblog post crasher (kdebug#202364)

* Mon Aug 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-3
- -libs subpkg to sanitize multilib

* Sun Aug 02 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-2
- fix to allow updating of status via microblog plasmoid 

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Wed Jul 22 2009 Than Ngo <than@redhat.com> - 4.2.98-1
- 4.3rc3

* Thu Jul 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.96-2
- BR: libXcomposite-devel (lancelot eye-candy)

* Sun Jul 12 2009 Than Ngo <than@redhat.com> - 4.2.96-1
- 4.3rc2

* Fri Jun 26 2009 Than Ngo <than@redhat.com> - 4.2.95-1
- 4.3rc1

* Thu Jun 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.90-1
- KDE-4.3 beta2 (4.2.90)

* Mon May 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.85-4
- BR: eigen2-devel soprano-devel

* Tue May 19 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.85-3
- BR kdeedu-devel (for Marble)

* Sun May 17 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.85-2
- Obsoletes/Provides: kde-plasma-weather

* Wed May 13 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.85-1
- KDE 4.3 beta 1

* Thu Apr 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-3
- disable contacts krunner by default

* Wed Apr 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-2
- optimize scriptlets

* Tue Mar 31 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-1
- KDE 4.2.2

* Mon Mar 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.1-3
- make bball applet work, ship .svg instead of .svgz (kdebug#185568)
- use new %%_qt45 macro
- spec housecleaning

* Fri Mar 13 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.1-2
- fix Lancelot rendering issues with Qt 4.5 (F11+ only, as the effect of that
  patch with 4.4.3 is unknown)

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.2.1-1
- 4.2.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0

* Wed Jan 07 2009 Than Ngo <than@redhat.com> - 4.1.96-1
- 4.2rc1

* Tue Dec 16 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.85-2
- saner versioned Obsoletes

* Fri Dec 12 2008 Than Ngo <than@redhat.com> 4.1.85-1
- 4.2beta2

* Tue Dec 02 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.80-3
- BR plasma-devel
- add Provides: kde-plasma-lancelot
- fix file list
- BR libkexiv2-devel >= 0.4.0 on F10+

* Thu Nov 20 2008 Than Ngo <than@redhat.com> 4.1.80-2
- merged
- add Obsoletes: kde-plasma-lancelot

* Thu Nov 20 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 4.1.80-1
- 4.1.80
- BR cmake >= 2.6.2
- make install/fast

* Wed Nov 12 2008 Than Ngo <than@redhat.com> 4.1.3-1
- 4.1.3

* Mon Sep 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-2
- make VERBOSE=1
- respin against new(er) kde-filesystem

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-1
- 4.1.2

* Fri Aug 29 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Wed Jul 23 2008 Than Ngo <than@redhat.com> 4.1.0-1
- 4.1.0

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-1
- 4.0.99

* Thu Jul 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-2
- kdeplasma-addons rename

* Fri Jul 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-1
- 4.0.98

* Thu Jul 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.85-2
- Provides: kdeplasma-addons

* Sun Jul 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.85-1
- 4.0.85

* Fri Jun 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.84-1
- 4.0.84

* Fri Jun 20 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.83-2
- add ldconfig to scriptlets

* Thu Jun 19 2008 Than Ngo <than@redhat.com> 4.0.83-1
- 4.0.83 (beta2)

* Sun Jun 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.82-1
- kdeplasmoids-4.0.82

* Tue May 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.80-2
- add missing BR openldap-devel
- update file list, add icon scriptlets

* Mon May 26 2008 Than Ngo <than@redhat.com> 4.0.80-1
- 4.1 beta 1

* Wed May 07 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.72-0.1.20080506svn804581
- update to revision 804581 from KDE SVN (to match KDE 4.0.72)
- add COPYING and COPYING.LIB as %%doc
- update file list

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.1-5
- rebuild (again) for the fixed %%{_kde4_buildtype}

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.1-4
- rebuild for NDEBUG and _kde4_libexecdir

* Tue Mar 04 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.1-3
- disable broken bluemarble applet (crashes Plasma when no OpenGL, #435656)

* Tue Mar 04 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.1-2
- rebuild against KDE 4.0.2 (mainly to make sure it still builds)

* Thu Jan 31 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-1
- kde-4.0.1

* Tue Jan 08 2008 Sebastian Vahl <fedora@deadbabylon.de> 4.0.0-1
- kde-4.0.0
