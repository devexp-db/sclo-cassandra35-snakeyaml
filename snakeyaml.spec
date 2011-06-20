
%global group_id  org.yaml

Name:             snakeyaml
Version:          1.8
Release:          6%{?dist}
Summary:          YAML parser and emitter for the Java programming language
License:          ASL 2.0
Group:            Development/Libraries
# http://code.google.com/p/snakeyaml
URL:              http://code.google.com/p/%{name}
# http://snakeyaml.googlecode.com/files/SnakeYAML-all-1.8.zip
Source0:          http://%{name}.googlecode.com/files/SnakeYAML-all-%{version}.zip
Source1:          %{name}.depmap

Patch0:           %{name}-spring-removal-workaround.patch
Patch1:           %{name}-gdata+base64coder+cobertura-addition.patch
Patch2:           %{name}-issue121-file-handle-leaks.patch
Patch3:           %{name}-add-osgi-metadata.patch

BuildArch:        noarch

BuildRequires:    java-devel
BuildRequires:    jpackage-utils
BuildRequires:    maven
BuildRequires:    maven-plugin-cobertura
BuildRequires:    maven-surefire-provider-junit4
BuildRequires:    joda-time
BuildRequires:    gnu-getopt
BuildRequires:    gdata-java
BuildRequires:    base64coder

Requires:         gdata-java
Requires:         base64coder
Requires:         java
Requires:         jpackage-utils
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

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
%patch2 -p1
%patch3 -p1

# remove bundled stuff
rm -rf target
rm -rf src/main/java/com
rm -rf src/main/java/biz

# convert CR+LF to LF
sed -i 's/\r//g' LICENSE.txt

%build
# gdata-java has no maven support -> depmap file needed
# http://code.google.com/p/gdata-java-client/issues/detail?id=328
mvn-rpmbuild -Dmaven.local.depmap.file="%{SOURCE1}" install

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap %{group_id} %{name} %{version} JPP %{name}

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%doc LICENSE.txt
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc LICENSE.txt
%doc %{_javadocdir}/%{name}

%changelog
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
