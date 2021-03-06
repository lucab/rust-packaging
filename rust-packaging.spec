%bcond_without check

Name:           rust-packaging
Version:        5
Release:        11%{?dist}
Summary:        RPM macros for building Rust packages on various architectures

License:        MIT
URL:            https://pagure.io/fedora-rust/rust2rpm
Source0:        https://releases.pagure.org/fedora-rust/rust2rpm/rust2rpm-%{version}.tar.xz
Patch0001:      0001-macros-remove-Cargo.lock.patch
Patch0002:      0002-macros-remove-spurious-whitespace.patch
Patch0003:      0003-macros-pass-__cargo_common_opts-to-cargo_install.patch
Patch0004:      0004-macros-make-cargo_-macros-parametric.patch
Patch0005:      0005-macros-remove-support-for-target-dir.patch

BuildArch:      noarch
ExclusiveArch:  %{rust_arches} noarch

# gawk is needed for stripping dev-deps in macro, 4.1.0 is needed for inplace feature
Requires:       gawk >= 4.1.0
Requires:       python3-rust2rpm = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       rust-srpm-macros = %{version}
Requires:       rust
Requires:       cargo
# Remove in F29
Obsoletes:      rust-rpm-macros < 2-2

%description
The package provides macros for building projects in Rust
on various architectures.

%package     -n python3-rust2rpm
Summary:        Convert Rust packages to RPM
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with check}
BuildRequires:  python3-pytest
BuildRequires:  cargo
BuildRequires:  python3-semantic_version
%endif
Requires:       cargo
Requires:       python3-semantic_version
Requires:       python3-jinja2
Requires:       python3-requests
Requires:       python3-tqdm
Obsoletes:      rust2rpm < 1-8
Provides:       rust2rpm = %{version}-%{release}
%{?python_provide:%python_provide python3-rust2rpm}

%description -n python3-rust2rpm
%{summary}.

%prep
%autosetup -n rust2rpm-%{version} -p1

%build
%py3_build

%install
%py3_install
install -D -p -m 0644 -t %{buildroot}%{_rpmmacrodir} data/macros.rust data/macros.cargo
install -D -p -m 0644 -t %{buildroot}%{_fileattrsdir} data/cargo.attr

%if %{with check}
%check
py.test-%{python3_version} -vv test.py
%endif

%files
%{_rpmmacrodir}/macros.rust
%{_rpmmacrodir}/macros.cargo
%{_fileattrsdir}/cargo.attr

%files -n python3-rust2rpm
%license LICENSE
%{_bindir}/rust2rpm
%{_bindir}/cargo-inspector
%{python3_sitelib}/rust2rpm-*.egg-info/
%{python3_sitelib}/rust2rpm/

%changelog
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 5-10
- Rebuilt for Python 3.7

* Mon Jul 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-9
- Rebuilt for Python 3.7

* Fri Jun 22 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-8
- Various improvements for %%cargo_* macros

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 5-7
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-6
- Pass %%__cargo_common_opts to %%cargo_install

* Tue Feb 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-5
- Explicitly require rust/cargo

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-3
- Fix syntax error

* Tue Jan 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-2
- Remove Cargo.lock

* Mon Jan 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-1
- Update to 5

* Sat Nov 04 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4-7
- Add Obsoletes for rust-rpm-macros

* Sat Nov 04 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4-6
- Use cp instead of install

* Sat Oct 21 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4-5
- Generate runtime dependencyon cargo for devel subpackages

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 08 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4-2
- Include license

* Sat Jul 08 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4-1
- Update to 4

* Fri Jun 23 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-5
- Explicitly set rustdoc path

* Wed Jun 21 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-4
- Mageia doesn't have C.UTF-8 lang

* Wed Jun 21 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-3
- Switch cargo_registry to /usr/share/cargo/registry

* Wed Jun 14 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-2
- Set C.UTF-8 for cargo inspector where python doesn't do locale coercing

* Tue Jun 13 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-1
- Initial package
