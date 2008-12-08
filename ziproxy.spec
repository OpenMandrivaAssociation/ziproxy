Summary:	A http compression and optimizer, non-caching, fully configurable proxy
Name:		ziproxy
Version:	2.6.0
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
BuildRequires:	libungif-devel
BuildRequires:	png-devel
BuildRequires:	X11-devel
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

rm -rf autom4te.cache configure
libtoolize --copy --force; aclocal -I config; autoheader; automake --foreign --add-missing --copy; autoconf

%configure2_5x \
    --with-gif=%{_prefix} \
    --with-jpeg=%{_prefix} \
    --with-png=%{_prefix} \
    --with-pthread=%{_prefix} \
    --with-jasper=%{_prefix} \
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
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/errors/*.html
%attr(0755,root,root) %{_sbindir}/%{name}
%attr(0755,root,root) %{_bindir}/ziproxylogtool
%attr(0755,root,root) %{_bindir}/ziproxy_genhtml_stats
%attr(0700,root,root) %dir /var/log/%{name}
%attr(0700,root,root) %dir /var/run/%{name}
%{_mandir}/man1/*
