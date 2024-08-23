from config import settings
from core.logger import log
from github import Github
from github import Auth
from core.exception import LockException

auth = Auth.Token(settings.GITHUB_TOKEN)
github_g = Github(auth=auth)
blog_repo = github_g.get_repo(settings.BLOG_REPO)

log.info(f"INITIALIZING BLOG REPO: {settings.BLOG_REPO} branch: {settings.BLOG_BRANCH}")


def check_build_status() -> bool:
    commits = blog_repo.get_commits()
    latest_commit = commits[0]
    check_suites = latest_commit.get_check_suites()
    for check_suite in check_suites:
        log.debug(
            f"Suite ID: {check_suite.id}, conclusion: {check_suite.conclusion}, time: {check_suite.updated_at} status: {check_suite.status}")
    log.info(f"Latest commit: {check_suites[-1].status}")  # queued in-progress completed
    if check_suites[-1].status == "completed":
        return True
    else:
        return False


def get_repo_blogs() -> list[str]:
    contents = blog_repo.get_contents(settings.BLOG_FOLDER_PATH)
    return [content_file.name for content_file in contents]


def get_blog_by_name(filename: str):  # return  base64
    blog = blog_repo.get_contents(f"{settings.BLOG_FOLDER_PATH}/{filename}")
    b64 = blog.content
    return b64


def delete_blog_by_name(filename: str):
    if not check_build_status:
        log.error("Build is not completed, please wait for the build to complete before deleting blog")
        raise LockException()
    file = blog_repo.get_contents(f"{settings.BLOG_FOLDER_PATH}/{filename}")
    sha = file.sha
    log.info(f"Deleting blog: {filename}")
    r = blog_repo.delete_file(
        path=f"{settings.BLOG_FOLDER_PATH}/{filename}",
        message=f"API Delete from manager",
        sha=sha,
    )
    return r


def create_new_blog(filename: str, file_content: str) -> ...:
    if not check_build_status:
        log.error("Build is not completed, please wait for the build to complete before deleting blog")
        raise LockException()
    r = blog_repo.create_file(
        path=f"{settings.BLOG_FOLDER_PATH}/{filename}",
        message=f"API Create from manager",
        content=file_content,
        branch=settings.BLOG_BRANCH,
    )
    return r
