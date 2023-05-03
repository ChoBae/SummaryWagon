"use client";
import styles from "./page.module.css";

export default function SearchBar() {
  return (
    <div className={styles.searchBox}>
      <h1 className={styles.slide}>🤔 What are you curious about? </h1>
      <input
        type="text"
        placeholder="Search.."
        onKeyUp={() => console.log("여기에 연관 검색어 로직 짜면 될듯")}
        // onkeyup={showRelatedKeywords(this.value)}
      />
      <div id="related-keywords"></div>
    </div>
  );
}
