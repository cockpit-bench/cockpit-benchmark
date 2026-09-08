"""Build small, separately labelled Android boundary candidates and exercise their behavior.

No canonical repository is touched. Host checks do not claim Android execution.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / 'scripts/verification'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rules import release, platform

FLEET = {'a1': '8155', 'a2': '8155', 'b1': '8295', 'b2': '8295'}

DOMAIN = '''package cabin.domain;
import java.io.InputStream;
import java.io.IOException;
import java.util.Properties;
public final class Fleet {
  private final Properties models = new Properties();
  public Fleet(InputStream source) throws IOException {
    if (source == null) throw new IOException("Missing fleet configuration");
    models.load(source);
  }
  public String page(String model, String platform) {
    if (!platform.equals(models.getProperty(model)))
      throw new IllegalArgumentException("Unsupported vehicle: " + model);
    return "Vehicle " + model + " on " + platform + ": " + models.getProperty("manual.page");
  }
}
'''
ACTIVITY = '''package cabin.ui;
import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;
import cabin.domain.Fleet;
import cabin.domain.Handbook;
public final class MainActivity extends Activity {
  @Override public void onCreate(Bundle state) {
    super.onCreate(state);
    TextView text = new TextView(this);
    String model = getIntent().getStringExtra("model");
    String platform = getIntent().getStringExtra("platform");
    try (java.io.InputStream input = getAssets().open("fleet.properties")) {
      String page = new Fleet(input).page(model == null ? "a1" : model, platform == null ? "8155" : platform);
      text.setText(new Handbook().display(page));
    } catch (java.io.IOException | IllegalArgumentException ex) {
      text.setText("Manual unavailable: " + ex.getMessage());
    }
    setContentView(text);
  }
}
'''
INTERFACE = 'package cabin.platform;\npublic interface DeviceInfo { String model(); }\n'
PUBLIC = '''package cabin.platform;
public final class AndroidDeviceInfo implements DeviceInfo {
  public String model() { return android.os.Build.MODEL; }
}
'''
COMPAT = '''package cabin.platform;
public final class AndroidDeviceInfo implements DeviceInfo {
  public String model() {
    try {
      Class<?> properties = Class.forName("android.os.SystemProperties");
      String value = (String) properties.getMethod("get", String.class).invoke(null, "ro.product.model");
      return value == null || value.isEmpty() ? "unknown" : value;
    } catch (ReflectiveOperationException | SecurityException ex) { return "unknown"; }
  }
}
'''
ISOLATED = '''package cabin.domain;
import cabin.platform.DeviceInfo;
import cabin.platform.AndroidDeviceInfo;
public final class Handbook {
  private final DeviceInfo device;
  public Handbook() { this(new AndroidDeviceInfo()); }
  public Handbook(DeviceInfo device) { this.device = java.util.Objects.requireNonNull(device); }
  public String display(String page) { return page + " [" + device.model() + "]"; }
}
'''
DIRECT = '''package cabin.domain;
public final class Handbook {
  public String display(String page) {
    String model;
    try {
      Class<?> properties = Class.forName("android.os.SystemProperties");
      model = (String) properties.getMethod("get", String.class).invoke(null, "ro.product.model");
    } catch (ReflectiveOperationException | SecurityException ex) { model = "unknown"; }
    return page + " [" + model + "]";
  }
}
'''


def command(*args, cwd=None):
    env = dict(os.environ, GIT_AUTHOR_DATE='2026-09-08T00:00:00Z', GIT_COMMITTER_DATE='2026-09-08T00:00:00Z',
               GIT_AUTHOR_NAME='Cabin Example Maintainer', GIT_COMMITTER_NAME='Cabin Example Maintainer',
               GIT_AUTHOR_EMAIL='example@invalid.local', GIT_COMMITTER_EMAIL='example@invalid.local')
    return subprocess.check_output([str(a) for a in args], cwd=cwd, env=env, stderr=subprocess.STDOUT).decode('utf-8', 'replace').strip()


def git(repo, *args):
    return command('git', '-c', 'user.name=Cabin Example Maintainer', '-c', 'user.email=example@invalid.local', '-C', repo, *args)


def write(repo, path, text):
    p = repo / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8', newline='\n')


def profile(repo, models, page):
    write(repo, 'app/src/main/assets/fleet.properties', ''.join(m+'='+FLEET[m]+'\n' for m in models) + 'manual.page='+page+'\n')


def seed(repo, mode):
    repo.mkdir(parents=True, exist_ok=False)
    git(repo, 'init', '-b', 'main')
    write(repo, '.gitattributes', '* -text\n')
    write(repo, 'settings.gradle', "pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }\ndependencyResolutionManagement { repositories { google(); mavenCentral() } }\nrootProject.name = 'CabinManual'\ninclude ':app'\n")
    write(repo, 'build.gradle', "plugins { id 'com.android.application' version '8.6.1' apply false }\n")
    write(repo, 'app/build.gradle', "plugins { id 'com.android.application' }\nandroid { namespace 'cabin.ui'; compileSdk 35\n defaultConfig { applicationId 'cabin.manual'; minSdk 31; targetSdk 35; versionCode 1; versionName '1.0.0' }\n}\n")
    write(repo, 'app/src/main/AndroidManifest.xml', '<manifest xmlns:android="http://schemas.android.com/apk/res/android"><application android:label="Cabin manual"><activity android:name="cabin.ui.MainActivity" android:exported="true"><intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter></activity></application></manifest>\n')
    write(repo, 'app/src/main/java/cabin/domain/Fleet.java', DOMAIN)
    write(repo, 'app/src/main/java/cabin/ui/MainActivity.java', ACTIVITY)
    write(repo, 'app/src/main/java/cabin/domain/Handbook.java', DIRECT if mode == 'direct' else ISOLATED)
    if mode != 'direct':
        write(repo, 'app/src/main/java/cabin/platform/DeviceInfo.java', INTERFACE)
        write(repo, 'app/src/main/java/cabin/platform/AndroidDeviceInfo.java', COMPAT if mode == 'compat' else PUBLIC)
    write(repo, 'README.md', '# Cabin manual\n\nThe Activity selects a vehicle manual from its packaged fleet configuration. Intent extras `model` and `platform` select the vehicle; unsupported combinations show an unavailable message.\n\nBuild with Gradle 8.7 / JDK 17 / Android SDK 35: `gradle :app:assembleDebug`. The SDK, Gradle and Maven dependencies are external prerequisites.\n')
    profile(repo, list(FLEET), 'Use park before changing cabin settings.')
    git(repo, 'add', '.')
    git(repo, 'commit', '-m', 'Implement fleet-selected cabin manual')


def validate_ref(repo, ref, mode, sdk, out):
    git(repo, 'checkout', '--quiet', ref)
    head = git(repo, 'rev-parse', 'HEAD')
    java = sorted((repo/'app/src/main/java').rglob('*.java'))
    compiled = []
    for api in (31, 35):
        target = out / ('api'+str(api))
        target.mkdir(parents=True)
        command('javac', '-encoding', 'UTF-8', '-source', '8', '-target', '8', '-classpath', sdk/'platforms'/('android-'+str(api))/'android.jar', '-d', target, *java)
        compiled.append(api)
    props = dict(line.split('=', 1) for line in (repo/'app/src/main/assets/fleet.properties').read_text().splitlines())
    # Host behavioral execution uses real domain sources; no replacement Android classes.
    checks = []
    for model, chip in FLEET.items():
        checks.append('check(f, "'+model+'", "'+chip+'", '+str(model in props).lower()+');')
    body = '''import cabin.domain.*; import java.io.*;
public class Check {
 static void check(Fleet f, String m, String p, boolean supported) {
   try { String s=f.page(m,p); if (!supported || !s.contains(m) || !s.contains(p)) throw new AssertionError(s); }
   catch(IllegalArgumentException ex) { if(supported) throw ex; }
 }
 public static void main(String[] a) throws Exception {
  Fleet f=new Fleet(a.length==0 ? Check.class.getClassLoader().getResourceAsStream("assets/fleet.properties") : new FileInputStream(a[0]));
  CHECKS
  check(f,"a1","incorrect",false); check(f,"unknown","8155",false);
  EXTRA
  System.out.println("PASS");
 }
}
'''.replace('CHECKS', '\n'.join(checks))
    if mode == 'direct':
        extra = 'if (!new Handbook().display("page").equals("page [unknown]")) throw new AssertionError();'
    else:
        extra = 'if (!new Handbook(() -> "test-device").display("page").equals("page [test-device]")) throw new AssertionError();'
        if mode == 'compat':
            extra += '\nif (!new cabin.platform.AndroidDeviceInfo().model().equals("unknown")) throw new AssertionError();'
    check = out/'Check.java'
    check.write_text(body.replace('EXTRA', extra))
    command('javac', '-classpath', out/'api35', '-d', out/'api35', check)
    # One production-only JAR is used for every accepted vehicle, not per-platform rebuilds.
    artifact = out/'cabin-manual.jar'
    command('jar', '--create', '--file', artifact, '--date=2026-09-08T00:00:00Z',
            '-C', out/'api35', 'cabin', '-C', repo/'app/src/main', 'assets')
    result = command('java', '-classpath', str(artifact)+os.pathsep+str(out/'api35'), 'Check')
    assert result == 'PASS'
    return {'ref': 'refs/heads/'+ref, 'head': head, 'tree': git(repo, 'rev-parse', 'HEAD^{tree}'), 'accepted_models': [m for m in FLEET if m in props], 'compiled_against_android_api': compiled, 'host_checks': 7 + (mode == 'compat'), 'android_runtime_executed': False,
            'production_jar_sha256': hashlib.sha256(artifact.read_bytes()).hexdigest(),
            'artifact_scope': 'Java production classes and fleet assets; not an APK'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--sdk', type=Path, default=Path(os.environ.get('ANDROID_HOME', str(Path(os.environ.get('LOCALAPPDATA', str(Path.home())))/'Android/Sdk'))))
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    results = []
    with tempfile.TemporaryDirectory(prefix='cabin-boundary-checks-') as temp:
        for name, strategy, mode in [('channel-a','none','public'), ('channel-b','vehicle','public'), ('channel-c','platform','public'), ('channel-d','unified','public'), ('channel-e','unified_trunk','public'), ('device-a','none','direct'), ('device-b','none','compat'), ('device-c','none','public')]:
            repo = args.output/'sources'/name
            repo.parent.mkdir(parents=True, exist_ok=True)
            seed(repo, mode)
            main_commit = git(repo, 'rev-parse', 'HEAD')
            branches = []
            if strategy == 'vehicle': branches = [('release/model-'+m+'-sop-2026', [m]) for m in FLEET]
            if strategy == 'platform': branches = [('platform/'+p, [m for m in FLEET if FLEET[m] == p]) for p in sorted(set(FLEET.values()))]
            if strategy == 'unified': branches = [('release/2026.1', list(FLEET))]
            for branch, models in branches:
                git(repo, 'checkout', '-b', branch, main_commit)
                profile(repo, models, 'Released manual: park before adjusting the cabin.')
                git(repo, 'add', '.')
                git(repo, 'commit', '-m', 'Publish manual for supported fleet')
            git(repo, 'checkout', 'main')
            if strategy == 'unified_trunk':
                git(repo, 'tag', '-a', 'v1.0.0', '-m', 'One cabin manual artifact for a1/a2 on 8155 and b1/b2 on 8295')
            refs = git(repo, 'for-each-ref', '--format=%(refname:short)', 'refs/heads').splitlines()
            checks = [validate_ref(repo, ref, mode, args.sdk, Path(temp)/name/ref.replace('/', '_')) for ref in refs]
            git(repo, 'checkout', 'main')
            assert not git(repo, 'status', '--porcelain') and not git(repo, 'remote')
            if name.startswith('channel'):
                facts = {'current_head_refs': [c['ref'] for c in checks], 'release_policy_evidence_verified': bool(branches) or strategy == 'unified_trunk', 'vehicle_specific_sop_channel': strategy == 'vehicle', 'platform_shared_release_channel': strategy == 'platform', 'cross_platform_unified_release_policy': strategy in {'unified','unified_trunk'}}
                prediction = release(facts)
                leaf = 'platform_reuse.release_branch_strategy'
            else:
                facts = dict(version_bound_status=1 if mode == 'compat' else 0, arch_bound_status=0, single_abi_closed_dependency_without_fallback=False, multiple_unstable_core_paths_without_isolation=False, permission_or_platform_hardcoding_blocks_core_migration=False, has_non_compatible_api=mode != 'public', non_compatible_api_all_covered=mode == 'compat', has_complex_permission_adaptation=False, has_arch_specific_deps=False, has_interface_abstraction=mode != 'direct', automated_compatibility_validation_at_least_two_android_versions=False, risks_all_localized_in_compat_layer=mode == 'compat', risk_fallback_available=mode in {'direct', 'compat'})
                prediction = platform(facts)
                leaf = 'platform_reuse.platform_upgrade'
            evidence = []
            for p in sorted((repo/'app/src/main').rglob('*')):
                if p.is_file(): evidence.append({'path': p.relative_to(repo).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'lines': len(p.read_text().splitlines())})
            tags = git(repo, 'for-each-ref', '--format=%(refname) %(objectname) %(*objectname)', 'refs/tags').splitlines()
            results.append({'case': name, 'family_id': 'cabin-manual-shared-origin-1', 'status': 'candidate_not_independently_adjudicated', 'head': main_commit, 'leaf': leaf, 'reviewed_facts': facts, 'rule_prediction': prediction, 'ref_behavior': checks, 'tags': tags, 'main_source_evidence': evidence})
            print(name, prediction, len(checks), 'refs validated', flush=True)
    (args.output/'candidates.json').write_text(json.dumps({'cases': results, 'canonical_member': False, 'independent_holdout': False, 'limits': ['Tiny behavioral prototypes, not production volume samples.', 'All eight share one family and must stay in one evaluation split.', 'javac API compilation and host execution do not establish APK build or Android runtime behavior.', 'Fact choices are explicit maintainer judgments; independent adjudication remains pending.']}, indent=2)+'\n')
    (args.output/'README.md').write_text('# Cabin boundary candidates\n\nEight small local repositories exercise release-channel and platform-isolation behaviors. `channel-e` has only main, a version tag and one production JAR shared by four vehicles across two platforms. `candidates.json` holds maintainer observations outside the sources. All variants share `cabin-manual-shared-origin-1` and must remain in one split. They are not part of Validation-18 or the pending 22 and are not independent gold.\n\nEach listed ref was compiled against Android SDK 31 and 35; real domain code was executed on the host JVM for allowed/rejected fleet combinations and display/fallback behavior. No APK or Android runtime test is claimed.\n', encoding='utf-8')


if __name__ == '__main__':
    main()
