
%global group_id  org.yaml

Name:             snakeyaml
Version:          1.11
Release:          5%{?dist}
Summary:          YAML parser and emitter for the Java programming language
License:          ASL 2.0
Group:            Development/Libraries
# http://code.google.com/p/snakeyaml
URL:              http://code.google.com/p/%{name}
# http://snakeyaml.googlecode.com/files/SnakeYAML-all-1.9.zip
Source0:          http://%{name}.googlecode.com/files/SnakeYAML-all-%{version}.zip

# Replace bundled Base64 implementation
# not upstreamable: http://code.google.com/p/snakeyaml/issues/detail?id=175
Patch0:           0001-Replace-bundled-base64-implementation.patch
# We don't have gdata-java-client in Fedora, use commons-codec instead
Patch1:           0002-Replace-bundled-gdata-java-client-classes-with-commo.patch

BuildArch:        noarch

BuildRequires:    java-devel
BuildRequires:    jpackage-utils
BuildRequires:    maven-local
BuildRequires:    maven-surefire-provider-junit4
BuildRequires:    cobertura
BuildRequires:    joda-time
BuildRequires:    gnu-getopt
BuildRequires:    base64coder
BuildRequires:    apache-commons-codec
%{?fedora:BuildRequires: springframework}

Requires:         java
Requires:         jpackage-utils
Requires:         base64coder
Requires:         apache-commons-codec

%description
SnakeYAML features:
    * a complete YAML 1.1 parser. In particular,
      SnakeYAML can parse all examples from the specification.
    * Unicode support including UTF-8/UTF-16 input/output.
    * high-level API for serializing and deserializing
      native Java objects.
    * support for all types from the YAML types repository.
    * relatively sensible error messages.


%package javadoc
Summary:          API documentation for %{name}
Group:            Documentation
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}

%patch0 -p1
%patch1 -p1

%pom_remove_plugin org.codehaus.mojo:cobertura-maven-plugin
%pom_add_dep net.sourceforge.cobertura:cobertura:any:test
sed -i "/<artifactId>spring</s/spring/&-core/" pom.xml
rm -f src/test/java/examples/SpringTest.java

# Replacement for bundled gdata-java-client
%pom_add_dep commons-codec:commons-codec

# remove bundled stuff
rm -rf target
rm -rf src/main/java/org/yaml/snakeyaml/external

# convert CR+LF to LF
sed -i 's/\r//g' LICENSE.txt

%if !0%{?fedora}
# Remove test dependencies because tests are skipped anyways.
%pom_xpath_remove "pom:dependency[pom:scope[text()='test']]"
%endif

%build
mvn-rpmbuild %{!?fedora:-Dmaven.test.skip=true} install

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%files
%doc LICENSE.txt
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc LICENSE.txt
%doc %{_javadocdir}/%{name}

%changelog
* Mon Apr 22 2013 Michal Srb <msrb@redhat.com> - 1.11-5
- Replace bundled base64 implementation
- Replace bundled gdata-java-client classes with apache-commons-codec

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-4
- Conditionally disable tests
- Conditionally remove test dependencies from POM

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.11-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Oct 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-1
- Update to upstream version 1.11

* Mon Oct 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-3
- Remove unneeded dependencies: base64coder, gdata-java
- Convert pom.xml patch to POM macro

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 20 2012 Mo Morsi <mmorsi@redhat.com> - 1.9-1
- Update to latest upstream release
- patch2, patch3 no longer needed
- update to latest fedora java guidelines

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Jaromir Capik <jcapik@redhat.com> - 1.8-6
- Patch for the issue67 test removed

* Fri Jun 17 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.8-5
- Add osgi metadata to jar file (#713935)

* Thu Jun 09 2011 Jaromir Capik <jcapik@redhat.com> - 1.8-4
- File handle leaks patched

* Tue Jun 07 2011 Jaromir Capik <jcapik@redhat.com> - 1.8-3
- base64coder-java renamed to base64coder

* Wed Jun 01 2011 Jaromir Capik <jcapik@redhat.com> - 1.8-2
- Bundled stuff removal

* Mon May 16 2011 Jaromir Capik <jcapik@redhat.com> - 1.8-1
- Initial version of the package
