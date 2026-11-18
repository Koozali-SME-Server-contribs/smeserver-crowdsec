%define name smeserver-crowdsec
%define version 0.9
%define release 6
Summary: This is what smeserver-crowdsec does.
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
Source: %{name}-%{version}.tar.gz
License: GNU GPL version 2
Group: SMEserver/addon
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
BuildArchitectures: noarch
BuildRequires: smeserver-devtools
Requires: smeserver-release >= 11.0
Requires: crowdsec
Requires: crowdsec-custom-bouncer
Requires: crowdsec-blocklist-mirror
Requires: crowdsec-firewall-bouncer-iptables
# TODO switch to crowdsec-firewall-bouncer-nftables when we move away iptables
Requires: yq
AutoReqProv: no

%description
SME Server wrapper for crowdsec

%changelog
* Wed Nov 18 2026 Jean-Philippe Pialasse <jpp@koozali.org> 0.9-6.sme
- prevent custom bouncer from starting if not enabled

* Tue Nov 17 2026 Jean-Philippe Pialasse <jpp@koozali.org> 0.9-5.sme
- parse sshd/sshd.log

* Tue Nov 17 2026 Jean-Philippe Pialasse <jpp@koozali.org> 0.9-4.sme
- improve parsing of logs : httpd, openvpn

* Mon Nov 16 2026 Jean-Philippe Pialasse <jpp@koozali.org> 0.9-3.sme
- fix service name type  for crowdsec-blocklist-mirror

* Wed Nov 11 2026 Jean-Philippe Pialasse <jpp@koozali.org> 0.9-2.sme
- fix ExecStartPre code

* Wed Jun 24 2026 Jean-Philippe Pialasse <jpp@koozali.org> 0.9-1.sme
- initial SME 11 build [SME: 13626]
- added our log path for dovecot
- added our qpsmtpd parser, scenarios and log path
- global templated whitelist
- enable roundcube crowdsecurity/vpatch-CVE-2025-49113
- ProFTP enabled
- handle creation of api key and registration of 3 basic bouncers

%prep

%setup -q

%build
perl createlinks

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-filelist
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT \
  --file /sbin/e-smith/systemd/crowdsec 'attr(755,root,root)' \
  --file /sbin/e-smith/systemd/crowdsec-blocklist-mirror 'attr(755,root,root)' \
  --file /sbin/e-smith/systemd/crowdsec-custom-bouncer 'attr(755,root,root)' \
  --file /sbin/e-smith/systemd/crowdsec-firewall 'attr(755,root,root)' \
> %{name}-%{version}-filelist
#echo "%doc COPYING"  >> %{name}-%{version}-filelist
#--dir <dir> 'attr(755,user,grp)' \
#--file <file> 'attr(755,root,root)' \

%clean
cd ..
rm -rf %{name}-%{version}

%pre

%preun

%post

%postun
#uninstall
%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
