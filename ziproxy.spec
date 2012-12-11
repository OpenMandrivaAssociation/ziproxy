Summary:	A http compression and optimizer, non-caching, fully configurable proxy
Name:		ziproxy
Version:	3.2.1
Release:	%mkrel 1
License:	GPL
Group:		System/Servers
URL:		http://ziproxy.sourceforge.net/
Source0:	http://www.dancab.com/proj/ziproxy/files/%{name}-%{version}.tar.bz2
Source1:        ziproxy.init
Source2:        ziproxy.sysconfig
Source3:        ziproxy.logrotate
Patch0:		ziproxy-mdv_conf.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	flex
BuildRequires:	jasper-devel
BuildRequires:	jpeg-devel
BuildRequires:	ungif-devel
BuildRequires:	png-devel
BuildRequires:	libsasl2-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Ziproxy is a forwarding (non-caching) proxy that gzips text and HTML files, and
reduces the size of images by converting them to lower quality JPEGs. It is
intended to increase the speed for low-speed Internet connections and it's
suitable for both home and professional usage. Ziproxy is fully configurable
and also features transparent proxy mode, preemptive name resolution, operation
in either daemon mode or (x)inetd mode, a detailed access log with compression
statistics, basic authentication, and more.

%prep

%setup -q
%patch0 -p0

cp %{SOURCE1} ziproxy.init
cp %{SOURCE2} ziproxy.sysconfig
cp %{SOURCE3} ziproxy.logrotate

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config/*.m4

%build
%serverbuild
autoreconf -fi
%configure2_5x \
    --with-jasper=%{_prefix} \
    --with-sasl2=%{_prefix} \
    --with-cfgfile=%{_sysconfdir}/ziproxy/ziproxy.conf

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_sysconfdir}/%{name}/errors
install -d %{buildroot}/var/log/%{name}
install -d %{buildroot}/var/run/%{name}
install -d %{buildroot}%{_mandir}/man1

install -m0755 src/%{name} %{buildroot}%{_sbindir}/%{name}
install -m0755 src/tools/ziproxylogtool %{buildroot}%{_bindir}/
install -m0755 src/tools/ziproxy_genhtml_stats.sh %{buildroot}%{_bindir}/ziproxy_genhtml_stats

install -m0644 etc/%{name}/%{name}.conf %{buildroot}%{_sysconfdir}/ziproxy/
install -m0644 var/%{name}/error/*.html %{buildroot}%{_sysconfdir}/ziproxy/errors/

install -m0755 ziproxy.init %{buildroot}%{_initrddir}/%{name}
install -m0644 ziproxy.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -m0644 ziproxy.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -m0644 man/*.1 %{buildroot}%{_mandir}/man1/

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING CREDITS ChangeLog JPEG2000.txt README README.tools
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0700,root,root) %dir %{_sysconfdir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%attr(0700,root,root) %dir %{_sysconfdir}/%{name}/errors
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/errors/*.html
%attr(0755,root,root) %{_sbindir}/%{name}
%attr(0755,root,root) %{_bindir}/ziproxylogtool
%attr(0755,root,root) %{_bindir}/ziproxy_genhtml_stats
%attr(0700,root,root) %dir /var/log/%{name}
%attr(0700,root,root) %dir /var/run/%{name}
%{_mandir}/man1/*


%changelog
* Sat Feb 11 2012 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.2.1-1mdv2012.0
+ Revision: 773361
- 3.2.1

* Fri Jan 21 2011 Funda Wang <fwang@mandriva.org> 3.2.0-2
+ Revision: 632000
- X is not required

* Wed Sep 08 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.2.0-1mdv2011.0
+ Revision: 576720
- libgsasl-devel as BR
- 3.2.0
- 3.2.0

* Sun Jul 18 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1.3-1mdv2011.0
+ Revision: 554766
- 3.1.3

* Fri Jul 09 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1.2-1mdv2011.0
+ Revision: 549863
- 3.1.2

* Tue Jun 15 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1.1-1mdv2010.1
+ Revision: 548071
- New 3.1.1

* Thu Jun 03 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1.0-1mdv2010.1
+ Revision: 547059
- New 3.1.0

* Fri May 21 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.0.1-1mdv2010.1
+ Revision: 545555
- 3.0.1

* Wed Apr 21 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.0.0-1mdv2010.1
+ Revision: 537289
- New 3.0
  P0 rediffed

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 2.7.2-1mdv2010.0
+ Revision: 451346
- 2.7.2

* Mon Aug 17 2009 Oden Eriksson <oeriksson@mandriva.com> 2.7.0-2mdv2010.0
+ Revision: 417299
- rebuilt against libjpeg v7

* Tue Apr 14 2009 Oden Eriksson <oeriksson@mandriva.com> 2.7.0-1mdv2009.1
+ Revision: 366863
- 2.7.0 (fixes US-CERT VU#435052)
- rediffed P0

* Mon Dec 08 2008 Oden Eriksson <oeriksson@mandriva.com> 2.6.0-1mdv2009.1
+ Revision: 311888
- 2.6.0
- rediffed P0

* Thu Sep 04 2008 Jérôme Soyer <saispo@mandriva.org> 2.5.2-1mdv2009.0
+ Revision: 280717
- New release

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild

* Tue Mar 11 2008 Oden Eriksson <oeriksson@mandriva.com> 2.5.1-1mdv2008.1
+ Revision: 185611
- 2.5.1

* Wed Jan 30 2008 Oden Eriksson <oeriksson@mandriva.com> 2.5.0-1mdv2008.1
+ Revision: 160265
- 2.5.0
- rediffed P0

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Oden Eriksson <oeriksson@mandriva.com> 2.4.3-1mdv2008.1
+ Revision: 120605
- 2.4.3

* Wed Dec 05 2007 Oden Eriksson <oeriksson@mandriva.com> 2.4.2-1mdv2008.1
+ Revision: 115580
- 2.4.2
- rediffed P0

  + Thierry Vignaud <tv@mandriva.org>
    - buildrequires X11-devel instead of XFree86-devel

* Sun Nov 25 2007 Oden Eriksson <oeriksson@mandriva.com> 2.4.1-1mdv2008.1
+ Revision: 111885
- import ziproxy


* Sun Nov 25 2007 Oden Eriksson <oeriksson@mandriva.com> 2.4.1-1mdv2008.1
- initial Mandriva package
