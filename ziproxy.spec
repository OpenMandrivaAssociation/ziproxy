Summary:	A http compression and optimizer, non-caching, fully configurable proxy
Name:		ziproxy
Version:	3.3.0
Release:	7
License:	GPLv2+
Group:		System/Servers
Url:		http://ziproxy.sourceforge.net/
Source0:	http://www.dancab.com/proj/ziproxy/files/%{name}-%{version}.tar.xz
Source1:	ziproxy.service
Source2:	ziproxy.sysconfig
Source3:	ziproxy.logrotate
Patch0:		ziproxy-mdv_conf.diff
Patch1:		ziproxy-3.2.1-gcc.patch
Patch2:		ziproxy-3.3.0-fix-configure.patch
Patch3:		ziproxy-3.3.0-giflib51.patch
BuildRequires:	flex
BuildRequires:	giflib-devel
BuildRequires:	jpeg-devel
BuildRequires:	sasl-devel
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(libpng)
Requires(post,preun):	rpm-helper

%description
Ziproxy is a forwarding (non-caching) proxy that gzips text and HTML files, and
reduces the size of images by converting them to lower quality JPEGs. It is
intended to increase the speed for low-speed Internet connections and it's
suitable for both home and professional usage. Ziproxy is fully configurable
and also features transparent proxy mode, preemptive name resolution, operation
in either daemon mode or (x)inetd mode, a detailed access log with compression
statistics, basic authentication, and more.

%files
%doc COPYING CREDITS ChangeLog JPEG2000.txt README README.tools
%attr(0644,root,root) %{_unitdir}/%{name}.service
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
%attr(0700,root,root) %dir /run/%{name}
%{_mandir}/man1/*

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

cp %{SOURCE1} ziproxy.service
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
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_sysconfdir}/%{name}/errors
install -d %{buildroot}/var/log/%{name}
install -d %{buildroot}/run/%{name}
install -d %{buildroot}%{_mandir}/man1

install -m0755 src/%{name} %{buildroot}%{_sbindir}/%{name}
install -m0755 src/tools/ziproxylogtool %{buildroot}%{_bindir}/
install -m0755 src/tools/ziproxy_genhtml_stats.sh %{buildroot}%{_bindir}/ziproxy_genhtml_stats

install -m0644 etc/%{name}/%{name}.conf %{buildroot}%{_sysconfdir}/ziproxy/
install -m0644 var/%{name}/error/*.html %{buildroot}%{_sysconfdir}/ziproxy/errors/

install -m0644 ziproxy.service -D %{buildroot}%{_unitdir}/%{name}.service
install -m0644 ziproxy.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -m0644 ziproxy.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -m0644 man/*.1 %{buildroot}%{_mandir}/man1/

sed "s:sysconfig:%{_sysconfdir}/sysconfig:" -i %{buildroot}%{_unitdir}/%{name}.service
